from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Application, Job


class JobAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title', 'company']
    list_display = ['title', 'company', 'owner']
    list_filter = ['remote_work', 'visa_sponsorship']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['queryset'] = User.objects.filter(
                Q(groups__name='Recruiter') | Q(is_superuser=True)
            ).distinct().order_by('username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ApplicationAdmin(admin.ModelAdmin):
    ordering = ['-applied_at']
    search_fields = ['user__username', 'job__title']
    list_display = ['user', 'job', 'status', 'applied_at']
    list_filter = ['status']


admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
