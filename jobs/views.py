from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ApplicationForm
from .models import Application, Job


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
