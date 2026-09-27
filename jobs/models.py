from django.db import models
from django.conf import settings


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=200, blank=True)
    skills_needed = models.TextField(blank=True, help_text='Separate your skills with commas')
    description = models.TextField(blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True, help_text='Yearly salary')

    remote_work = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs_owned')

    def __str__(self):
        return f'{self.title} at {self.company}'


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'applied', 'Applied'
        REVIEWED = 'reviewed', 'Reviewed'
        INTERVIEW = 'interview', 'Interview'
        OFFER = 'offer', 'Offer'
        CLOSED = 'closed', 'Closed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    note = models.TextField(max_length=1000)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.APPLIED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'job'], name='unique_user_job_application'),
        ]

    def __str__(self):
        return f'{self.user} applied to {self.job}'
