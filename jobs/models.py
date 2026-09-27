from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=200, blank=True)
    skills_needed = models.TextField(blank=True, help_text='Separate your skills with commas')
    description = models.TextField(blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True, help_text='Yearly salary')

    remote_work = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} at {self.company}'
