from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import get_profile, require_role
from accounts.models import Profile, Role

from .forms import ApplicationForm, ApplicationStatusForm, JobForm, SavedSearchForm
from .models import Application, Job, JobStatus, Notification, SavedSearch
from .services import (
    filter_candidates,
    filters_from_request,
    recommend_candidates_for_job,
    visible_seeker_queryset,
)


def job_list(request):
    jobs = Job.objects.filter(status=JobStatus.ACTIVE).prefetch_related('skills')

    q = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    skills = request.GET.get('skills', '').strip()
    work_model = request.GET.get('work_model', '').strip()
    visa = request.GET.get('visa', '').strip()
    salary_min = request.GET.get('salary_min', '').strip()
    salary_max = request.GET.get('salary_max', '').strip()
    sort = request.GET.get('sort', 'newest').strip()

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q)
            | Q(company__icontains=q)
            | Q(description__icontains=q)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if skills:
        for skill in [s.strip() for s in skills.split(',') if s.strip()]:
            jobs = jobs.filter(skills__name__icontains=skill)
    if work_model:
        jobs = jobs.filter(work_model=work_model)
    if visa:
        jobs = jobs.filter(visa_sponsorship=visa)
    if salary_min.isdigit():
        jobs = jobs.filter(
            Q(salary_max__gte=int(salary_min)) | Q(salary_min__gte=int(salary_min))
        )
    if salary_max.isdigit():
        jobs = jobs.filter(
            Q(salary_min__lte=int(salary_max)) | Q(salary_max__lte=int(salary_max))
        )

    jobs = jobs.distinct()
    if sort == 'salary':
        jobs = jobs.order_by('-salary_max', '-salary_min', '-updated_at')
    else:
        jobs = jobs.order_by('-created_at')

    template_data = {
        'title': 'Jobs',
        'jobs': jobs,
        'filters': {
            'q': q,
            'location': location,
            'skills': skills,
            'work_model': work_model,
            'visa': visa,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'sort': sort,
        },
        'result_count': jobs.count(),
    }
    return render(request, 'jobs/job_list.html', {'template_data': template_data})


def job_detail(request, pk):
    job = get_object_or_404(
        Job.objects.prefetch_related('skills'), pk=pk
    )
    profile = get_profile(request.user) if request.user.is_authenticated else None
    can_view = job.status == JobStatus.ACTIVE or (
        profile and (job.owner_id == request.user.id or profile.role == Role.ADMIN)
    )
    if not can_view:
        messages.error(request, 'This job is not available.')
        return redirect('jobs.list')

    existing = None
    if request.user.is_authenticated and profile and profile.role == Role.SEEKER:
        existing = Application.objects.filter(seeker=request.user, job=job).first()

    template_data = {
        'title': job.title,
        'job': job,
        'existing_application': existing,
        'apply_form': ApplicationForm(),
        'can_apply': (
            profile
            and profile.role == Role.SEEKER
            and job.status == JobStatus.ACTIVE
            and existing is None
        ),
    }
    return render(request, 'jobs/job_detail.html', {'template_data': template_data})


@require_role(Role.SEEKER)
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk, status=JobStatus.ACTIVE)
    if Application.objects.filter(seeker=request.user, job=job).exists():
        messages.info(request, 'You already applied to this job.')
        return redirect('jobs.detail', pk=job.pk)

    if request.method != 'POST':
        return redirect('jobs.detail', pk=job.pk)

    form = ApplicationForm(request.POST)
    if form.is_valid():
        application = form.save(commit=False)
        application.seeker = request.user
        application.job = job
        application.save()
        Notification.objects.create(
            user=job.owner,
            notification_type='application',
            message=f'{request.user.get_full_name() or request.user.username} applied to {job.title}',
            link=f'/recruiter/jobs/{job.pk}/applicants/',
        )
        messages.success(request, 'Application submitted.')
        return redirect('jobs.applications')

    messages.error(request, 'Could not submit application.')
    return redirect('jobs.detail', pk=job.pk)


@require_role(Role.SEEKER)
def applications_list(request):
    status = request.GET.get('status', '').strip().upper()
    apps = (
        Application.objects.filter(seeker=request.user)
        .select_related('job')
        .order_by('-updated_at')
    )
    if status:
        apps = apps.filter(status=status)

    template_data = {
        'title': 'Applications',
        'applications': apps,
        'current_status': status,
        'statuses': [
            ('', 'All'),
            ('APPLIED', 'Applied'),
            ('REVIEW', 'Review'),
            ('INTERVIEW', 'Interview'),
            ('OFFER', 'Offer'),
            ('CLOSED', 'Closed'),
        ],
    }
    return render(
        request, 'jobs/applications.html', {'template_data': template_data}
    )


@require_role(Role.SEEKER)
def application_detail(request, pk):
    application = get_object_or_404(
        Application.objects.select_related('job'),
        pk=pk,
        seeker=request.user,
    )
    template_data = {
        'title': f'Application · {application.job.title}',
        'application': application,
    }
    return render(
        request, 'jobs/application_detail.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def recruiter_jobs(request):
    jobs = (
        Job.objects.filter(owner=request.user)
        .annotate(app_count=Count('applications'))
        .order_by('-updated_at')
    )
    template_data = {
        'title': 'My jobs',
        'jobs': jobs,
    }
    return render(
        request, 'jobs/recruiter_jobs.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def recruiter_job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            form._save_skills(job)
            messages.success(request, 'Job created.')
            return redirect('jobs.recruiter_jobs')
    else:
        form = JobForm(
            initial={
                'company': get_profile(request.user).company,
                'status': JobStatus.DRAFT,
            }
        )

    template_data = {'title': 'Post a job', 'form': form}
    return render(request, 'jobs/job_form.html', {'template_data': template_data})


@require_role(Role.RECRUITER)
def recruiter_job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated.')
            return redirect('jobs.recruiter_jobs')
    else:
        form = JobForm(instance=job)

    template_data = {'title': 'Edit job', 'form': form, 'job': job}
    return render(request, 'jobs/job_form.html', {'template_data': template_data})


@require_role(Role.RECRUITER)
def recruiter_job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, owner=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted.')
        return redirect('jobs.recruiter_jobs')
    template_data = {'title': 'Delete job', 'job': job}
    return render(
        request, 'jobs/job_confirm_delete.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def recruiter_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk, owner=request.user)
    applications = (
        Application.objects.filter(job=job)
        .select_related('seeker', 'seeker__profile')
        .order_by('-updated_at')
    )
    selected_id = request.GET.get('app')
    selected = None
    if selected_id:
        selected = applications.filter(pk=selected_id).first()
    if selected is None and applications.exists():
        selected = applications.first()

    status_form = None
    if selected:
        if request.method == 'POST':
            status_form = ApplicationStatusForm(request.POST, instance=selected)
            if status_form.is_valid():
                app = status_form.save(commit=False)
                app.status_updated_at = timezone.now()
                app.save()
                Notification.objects.create(
                    user=selected.seeker,
                    notification_type='status',
                    message=f'Your application for {job.title} is now {selected.get_status_display()}.',
                    link=f'/applications/{selected.pk}/',
                )
                messages.success(request, 'Application status updated.')
                return redirect(
                    f"{request.path}?app={selected.pk}"
                )
        else:
            status_form = ApplicationStatusForm(instance=selected)

    recommendations = recommend_candidates_for_job(job)

    template_data = {
        'title': f'Applicants · {job.title}',
        'job': job,
        'applications': applications,
        'selected': selected,
        'status_form': status_form,
        'recommendations': recommendations,
    }
    return render(
        request, 'jobs/applicants.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def candidates(request):
    filters = filters_from_request(request)
    queryset = visible_seeker_queryset(request.user)
    queryset = filter_candidates(queryset, filters)

    sort = request.GET.get('sort', 'relevance')
    if sort == 'updated':
        queryset = queryset.order_by('-updated_at')
    else:
        queryset = queryset.order_by('-updated_at')

    template_data = {
        'title': 'Candidates',
        'candidates': queryset,
        'filters': filters,
        'result_count': queryset.count(),
        'sort': sort,
    }
    return render(request, 'jobs/candidates.html', {'template_data': template_data})


@require_role(Role.RECRUITER)
def candidate_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk, role=Role.SEEKER)
    if not profile.is_visible_to_recruiter(request.user):
        messages.error(request, 'This candidate profile is not visible.')
        return redirect('jobs.candidates')

    applications = Application.objects.filter(
        seeker=profile.user, job__owner=request.user
    ).select_related('job')

    template_data = {
        'title': profile.display_name,
        'profile': profile,
        'applications': applications,
    }
    return render(
        request, 'jobs/candidate_detail.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def saved_searches(request):
    searches = SavedSearch.objects.filter(recruiter=request.user)
    template_data = {
        'title': 'Saved searches',
        'searches': searches,
    }
    return render(
        request, 'jobs/saved_searches.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def saved_search_create(request):
    filters = filters_from_request(request)
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.recruiter = request.user
            search.filters = filters
            search.save()
            messages.success(request, 'Search saved.')
            return redirect('jobs.saved_searches')
    else:
        form = SavedSearchForm(initial={'notify_in_app': True})

    match_count = filter_candidates(
        visible_seeker_queryset(request.user), filters
    ).count()

    template_data = {
        'title': 'Save search',
        'form': form,
        'filters': filters,
        'match_count': match_count,
    }
    return render(
        request, 'jobs/saved_search_form.html', {'template_data': template_data}
    )


@require_role(Role.RECRUITER)
def saved_search_run(request, pk):
    search = get_object_or_404(SavedSearch, pk=pk, recruiter=request.user)
    params = '&'.join(
        f'{k}={v}' for k, v in (search.filters or {}).items() if v
    )
    url = '/candidates/'
    if params:
        url = f'{url}?{params}'
    return redirect(url)


@require_role(Role.RECRUITER)
def saved_search_delete(request, pk):
    search = get_object_or_404(SavedSearch, pk=pk, recruiter=request.user)
    if request.method == 'POST':
        search.delete()
        messages.success(request, 'Saved search deleted.')
    return redirect('jobs.saved_searches')


@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user)
    if request.method == 'POST' and request.POST.get('action') == 'mark_all':
        notes.filter(is_read=False).update(is_read=True)
        messages.success(request, 'All alerts marked as read.')
        return redirect('jobs.notifications')

    template_data = {
        'title': 'Alerts',
        'notifications': notes[:50],
    }
    return render(
        request, 'jobs/notifications.html', {'template_data': template_data}
    )


@login_required
def notification_read(request, pk):
    note = get_object_or_404(Notification, pk=pk, user=request.user)
    note.is_read = True
    note.save(update_fields=['is_read'])
    if note.link:
        return redirect(note.link)
    return redirect('jobs.notifications')
