from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile


def split_skills(text):
    return [skill.strip() for skill in (text or '').split(',') if skill.strip()]


def matching_skills(wanted_text, have_text):
    wanted = {skill.lower() for skill in split_skills(wanted_text)}
    if not wanted:
        return []
    return [skill for skill in split_skills(have_text) if skill.lower() in wanted]


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


class SavedSearch(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
    skills = models.CharField(max_length=255, blank=True, help_text='Separate skills with commas')
    created_at = models.DateTimeField(auto_now_add=True)
    notified_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='+')

    def __str__(self):
        return f'{self.recruiter}: {self.skills}'


class Notification(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    subject = models.CharField(max_length=255, default='You have a new match!')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


@receiver(post_save, sender=Profile)
def notify_saved_searches(instance, **kwargs):
    profile = instance
    if not profile.show_skills_to_recruiters or not profile.skills:
        return

    for saved_search in SavedSearch.objects.exclude(notified_users=profile.user):
        matches = matching_skills(saved_search.skills, profile.skills)
        if not matches:
            continue
        Notification.objects.create(
            recruiter=saved_search.recruiter,
            description=(
                f'{profile.user.get_username()} seems like a good fit for your saved search '
                f'({saved_search.skills}). They have {", ".join(matches)}.'
            ),
        )
        saved_search.notified_users.add(profile.user)
