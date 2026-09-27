from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=160, blank=True)
    skills = models.TextField(blank=True, help_text='Separate skills with commas')
    education = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    links = models.TextField(blank=True, help_text='Add links, one per line')

    def __str__(self):
        return self.user.get_username()
