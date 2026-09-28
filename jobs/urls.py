from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('applications/', views.applications, name='jobs.applications'),
    path('<int:job_id>/apply/', views.apply, name='jobs.apply'),
    path('mine/', views.recruiter_jobs, name='jobs.recruiter_jobs'),
    path('mine/<int:job_id>/', views.job_detail, name='jobs.job_detail'),
    path('<int:job_id>/applicants/', views.applicants, name='jobs.applicants'),
    path('applicants/<int:application_id>/status/', views.review_application_status, name='jobs.review_application_status'),
    path('candidates/', views.candidate_search, name='jobs.candidate_search'),
    path('candidates/save/', views.save_search, name='jobs.save_search'),
    path('notifications/', views.notifications, name='jobs.notifications'),
    path('mine/new/', views.create_job, name='jobs.create_job'),
    path('mine/<int:job_id>/edit/', views.edit_job, name='jobs.edit_job'),
]
