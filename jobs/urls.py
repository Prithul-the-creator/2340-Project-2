from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('applications/', views.applications, name='jobs.applications'),
    path('applications/<int:application_id>/status/', views.update_application_status, name='jobs.update_application_status'),
    path('<int:job_id>/apply/', views.apply, name='jobs.apply'),
]
