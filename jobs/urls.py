from django.urls import path

from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='jobs.list'),
    path('jobs/<int:pk>/', views.job_detail, name='jobs.detail'),
    path('jobs/<int:pk>/apply/', views.apply_to_job, name='jobs.apply'),
    path('applications/', views.applications_list, name='jobs.applications'),
    path(
        'applications/<int:pk>/',
        views.application_detail,
        name='jobs.application_detail',
    ),
    path('recruiter/jobs/', views.recruiter_jobs, name='jobs.recruiter_jobs'),
    path(
        'recruiter/jobs/new/',
        views.recruiter_job_create,
        name='jobs.recruiter_job_create',
    ),
    path(
        'recruiter/jobs/<int:pk>/',
        views.recruiter_job_edit,
        name='jobs.recruiter_job_edit',
    ),
    path(
        'recruiter/jobs/<int:pk>/delete/',
        views.recruiter_job_delete,
        name='jobs.recruiter_job_delete',
    ),
    path(
        'recruiter/jobs/<int:pk>/applicants/',
        views.recruiter_applicants,
        name='jobs.applicants',
    ),
    path(
        'recruiter/jobs/<int:pk>/invite/<int:profile_pk>/',
        views.invite_candidate,
        name='jobs.invite_candidate',
    ),
    path(
        'recruiter/jobs/<int:pk>/dismiss/<int:profile_pk>/',
        views.dismiss_recommendation,
        name='jobs.dismiss_recommendation',
    ),
    path(
        'recruiter/jobs/<int:pk>/restore-recommendations/',
        views.restore_recommendations,
        name='jobs.restore_recommendations',
    ),
    path('candidates/', views.candidates, name='jobs.candidates'),
    path('candidates/<int:pk>/', views.candidate_detail, name='jobs.candidate_detail'),
    path('saved-searches/', views.saved_searches, name='jobs.saved_searches'),
    path(
        'saved-searches/new/',
        views.saved_search_create,
        name='jobs.saved_search_create',
    ),
    path(
        'saved-searches/<int:pk>/edit/',
        views.saved_search_edit,
        name='jobs.saved_search_edit',
    ),
    path(
        'saved-searches/<int:pk>/run/',
        views.saved_search_run,
        name='jobs.saved_search_run',
    ),
    path(
        'saved-searches/<int:pk>/delete/',
        views.saved_search_delete,
        name='jobs.saved_search_delete',
    ),
    path('alerts/', views.notifications, name='jobs.notifications'),
    path(
        'alerts/<int:pk>/',
        views.notification_read,
        name='jobs.notification_read',
    ),
]
