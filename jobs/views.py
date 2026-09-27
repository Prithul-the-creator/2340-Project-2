from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Job


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
                job_matches = job_matches.filter(skills__icontains=skill.strip())
    if place_desired:
        job_matches = job_matches.filter(location__icontains=place_desired)
    if pay_floor.isdigit():
        job_matches = job_matches.filter(salary__gte=int(pay_floor))
    if work_env == 'remote':
        job_matches = job_matches.filter(remote=True)
    elif work_env == 'onsite':
        job_matches = job_matches.filter(remote=False)
    if request.GET.get('visa') == 'yes':
        job_matches = job_matches.filter(visa_sponsorship=True)

    return render(request, 'jobs/job_search.html', {
        'template_data': template_data, 'jobs': job_matches, 'filters': request.GET,
    })


@login_required
def applications(request):
    template_data = {'title': 'Applications'}
    
    return render(request, 'jobs/applications.html', {'template_data': template_data})
