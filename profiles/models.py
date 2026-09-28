from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=160, blank=True)
    skills = models.TextField(blank=True, help_text='Separate skills with commas')
    education = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    projects = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    links = models.TextField(blank=True, help_text='Add links, one per line')
    show_headline_to_recruiters = models.BooleanField(default=True)
    show_skills_to_recruiters = models.BooleanField(default=True)
    show_education_to_recruiters = models.BooleanField(default=True)
    show_work_experience_to_recruiters = models.BooleanField(default=True)
    show_links_to_recruiters = models.BooleanField(default=True)
    show_location_to_recruiters = models.BooleanField(default=True)
    show_projects_to_recruiters = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_username()
