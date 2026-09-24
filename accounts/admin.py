from django.contrib import admin

from .models import Education, Experience, Link, Profile, Project, Skill


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status', 'privacy', 'location')
    list_filter = ('role', 'status', 'privacy')
    search_fields = ('user__username', 'user__email', 'headline')
    filter_horizontal = ('skills',)
    inlines = [EducationInline, ExperienceInline, ProjectInline, LinkInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ('name',)
