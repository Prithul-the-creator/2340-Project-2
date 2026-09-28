from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from profiles.models import Profile

from .forms import ApplicationForm
from .models import Application, Job, Notification, SavedSearch, matching_skills

PROFILE_FIELDS = [
    ('headline', 'Headline', 'show_headline_to_recruiters'),
    ('skills', 'Skills', 'show_skills_to_recruiters'),
    ('education', 'Education', 'show_education_to_recruiters'),
    ('work_experience', 'Experience', 'show_work_experience_to_recruiters'),
    ('links', 'Links', 'show_links_to_recruiters'),
]


def visible_profile_fields(profile):
    if profile is None:
        return []
    fields = []
    for field, label, show_flag in PROFILE_FIELDS:
        value = getattr(profile, field)
        if getattr(profile, show_flag) and value:
            fields.append((label, value))
    return fields


def index(request):
    template_data = {'title': 'Jobs'}
    job_matches = Job.objects.all()
    title_search = request.GET.get('title', '').strip()
    skills_desired = request.GET.get('skills', '').strip()
    place_desired = request.GET.get('location', '').strip()
    pay_floor = request.GET.get('min_salary', '').strip()
    work_env = request.GET.get('work_type', '')

    if title_search:
        job_matches = job_matches.filter(title__icontains=title_search)
    if skills_desired:
        for skill in skills_desired.split(','):
            if skill.strip():
                job_matches = job_matches.filter(skills_needed__icontains=skill.strip())
    if place_desired:
        job_matches = job_matches.filter(location__icontains=place_desired)
    if pay_floor.isdigit():
        job_matches = job_matches.filter(salary__gte=int(pay_floor))
    if work_env == 'remote':
        job_matches = job_matches.filter(remote_work=True)
    elif work_env == 'onsite':
        job_matches = job_matches.filter(remote_work=False)
    if request.GET.get('visa') == 'yes':
        job_matches = job_matches.filter(visa_sponsorship=True)

    return render(request, 'jobs/job_search.html', {
        'template_data': template_data,
        'jobs': job_matches,
        'filters': request.GET,
        'applied_job_ids': set(Application.objects.filter(user=request.user).values_list('job_id', flat=True))
        if request.user.is_authenticated else set(),
    })


@login_required
@require_POST
def apply(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    form = ApplicationForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please add a note of up to 1,000 characters before applying.')
        return redirect('jobs.index')

    application, created = Application.objects.get_or_create(
        user=request.user,
        job=job,
        defaults={'note': form.cleaned_data['note']},
    )
    if created:
        messages.success(request, f'Your application to {job.title} at {job.company} was sent.')
    else:
        messages.info(request, 'You have already applied to this job.')
    return redirect('jobs.applications')


@login_required
def applications(request):
    template_data = {'title': 'Applications'}
    seeker_applications = Application.objects.filter(user=request.user).select_related('job').order_by('-applied_at')

    return render(request, 'jobs/applications.html', {
        'template_data': template_data,
        'applications': seeker_applications,
        'status_choices': Application.Status.choices,
    })


@login_required
@require_POST
def update_application_status(request, application_id):
    application = get_object_or_404(Application, pk=application_id, user=request.user)
    status = request.POST.get('status')
    if status not in Application.Status.values:
        messages.error(request, 'Choose a valid application status.')
    else:
        application.status = status
        application.save(update_fields=['status'])
        messages.success(request, 'Application status updated.')
    return redirect('jobs.applications')


@login_required
@permission_required('jobs.view_application', raise_exception=True)
def recruiter_jobs(request):
    template_data = {'title': 'My Jobs'}
    owned_jobs = Job.objects.filter(owner=request.user).annotate(applicant_count=Count('applications')).order_by('title')

    return render(request, 'jobs/recruiter_jobs.html', {
        'template_data': template_data,
        'jobs': owned_jobs,
    })


@login_required
@permission_required('jobs.view_application', raise_exception=True)
def applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id, owner=request.user)
    template_data = {'title': f'Applicants for {job.title}'}
    job_applications = list(job.applications.select_related('user').order_by('-applied_at'))
    applicant_ids = []
    for application in job_applications:
        applicant_ids.append(application.user_id)

    profiles = {}
    for profile in Profile.objects.filter(user_id__in=applicant_ids):
        profiles[profile.user_id] = profile

    reviews = []
    for application in job_applications:
        reviews.append({
            'application': application,
            'profile_fields': visible_profile_fields(profiles.get(application.user_id)),
        })

    return render(request, 'jobs/applicants.html', {'template_data': template_data, 'job': job, 'reviews': reviews, 'status_choices': Application.Status.choices})


@login_required
@permission_required('jobs.change_application', raise_exception=True)
@require_POST
def review_application_status(request, application_id):
    application = get_object_or_404(Application, pk=application_id, job__owner=request.user)
    status = request.POST.get('status')
    if status not in Application.Status.values:
        messages.error(request, 'Choose a valid application status.')
    else:
        application.status = status
        application.save(update_fields=['status'])
        messages.success(request, f'Updated {application.user.username} to {application.get_status_display()}.')
    return redirect('jobs.applicants', job_id=application.job_id)


@login_required
@permission_required('jobs.view_application', raise_exception=True)
def candidate_search(request):
    template_data = {'title': 'Find Candidates'}
    skills_wanted = request.GET.get('skills', '').strip()

    candidates = []
    profiles = Profile.objects.filter(show_skills_to_recruiters=True).exclude(skills='').select_related('user')
    for profile in profiles:
        matches = matching_skills(skills_wanted, profile.skills) if skills_wanted else []
        if skills_wanted and not matches:
            continue
        candidates.append({'profile': profile, 'matches': matches})

    return render(request, 'jobs/candidate_search.html', {
        'template_data': template_data,
        'candidates': candidates,
        'filters': request.GET,
    })


@login_required
@permission_required('jobs.view_application', raise_exception=True)
@require_POST
def save_search(request):
    skills_wanted = request.GET.get('skills', '').strip()
    SavedSearch.objects.get_or_create(recruiter=request.user, skills=skills_wanted)
    messages.success(request, 'Search saved. We\'ll notify you about new matches.')
    return redirect(f"{reverse('jobs.candidate_search')}?skills={skills_wanted}")


@login_required
@permission_required('jobs.view_application', raise_exception=True)
def notifications(request):
    template_data = {'title': 'Notifications'}
    recruiter_notifications = list(Notification.objects.filter(recruiter=request.user))
    Notification.objects.filter(recruiter=request.user, is_read=False).update(is_read=True)

    return render(request, 'jobs/notifications.html', {
        'template_data': template_data,
        'notifications': recruiter_notifications,
    })


@login_required
@permission_required('jobs.view_application', raise_exception=True)
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id, owner=request.user)
    template_data = {'title': job.title}

    recommendations = []
    profiles = Profile.objects.filter(show_skills_to_recruiters=True).exclude(skills='').select_related('user')
    for profile in profiles:
        matches = matching_skills(job.skills_needed, profile.skills)
        if matches:
            recommendations.append({'profile': profile, 'matches': matches})

    return render(request, 'jobs/job_detail.html', {
        'template_data': template_data,
        'job': job,
        'recommendations': recommendations,
    })