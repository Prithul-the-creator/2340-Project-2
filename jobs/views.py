from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    template_data = {'title': 'Jobs'}
    return render(request, 'jobs/index.html', {'template_data': template_data})


@login_required
def applications(request):
    template_data = {'title': 'Applications'}
    return render(request, 'jobs/applications.html', {'template_data': template_data})
