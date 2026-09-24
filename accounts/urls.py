from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('profile/', views.profile_view, name='accounts.profile'),
    path('profile/edit/', views.profile_edit, name='accounts.profile_edit'),
    path('profile/education/add/', views.education_add, name='accounts.education_add'),
    path(
        'profile/education/<int:pk>/delete/',
        views.education_delete,
        name='accounts.education_delete',
    ),
    path(
        'profile/experience/add/',
        views.experience_add,
        name='accounts.experience_add',
    ),
    path(
        'profile/experience/<int:pk>/delete/',
        views.experience_delete,
        name='accounts.experience_delete',
    ),
    path('profile/project/add/', views.project_add, name='accounts.project_add'),
    path(
        'profile/project/<int:pk>/delete/',
        views.project_delete,
        name='accounts.project_delete',
    ),
    path('profile/link/add/', views.link_add, name='accounts.link_add'),
    path(
        'profile/link/<int:pk>/delete/',
        views.link_delete,
        name='accounts.link_delete',
    ),
    path('settings/privacy/', views.privacy_settings, name='accounts.privacy'),
]
