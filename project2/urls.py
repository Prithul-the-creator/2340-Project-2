from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('jobs.urls')),
    path('manage/users/', accounts_views.manage_users, name='accounts.manage_users'),
    path(
        'manage/users/<int:user_id>/',
        accounts_views.manage_user_detail,
        name='accounts.manage_user_detail',
    ),
    path('manage/roles/', accounts_views.manage_roles, name='accounts.manage_roles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
