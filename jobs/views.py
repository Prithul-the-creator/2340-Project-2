from django.shortcuts import render


def index(request):
    template_data = {'title': 'Jobs'}
    return render(request, 'jobs/index.html', {'template_data': template_data})
