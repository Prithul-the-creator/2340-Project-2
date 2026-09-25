from django.contrib import admin

from .models import (
    Application,
    DismissedRecommendation,
    Job,
    Notification,
    SavedSearch,
)


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ('seeker', 'created_at')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'owner', 'status', 'updated_at')
    list_filter = ('status', 'work_model', 'visa_sponsorship')
    search_fields = ('title', 'company', 'location')
    filter_horizontal = ('skills',)
    inlines = [ApplicationInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('seeker', 'job', 'status', 'updated_at')
    list_filter = ('status',)
    search_fields = ('seeker__username', 'job__title')


@admin.register(DismissedRecommendation)
class DismissedRecommendationAdmin(admin.ModelAdmin):
    list_display = ('job', 'profile', 'created_at')


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'recruiter', 'notify_in_app', 'notify_email', 'updated_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'notification_type')
