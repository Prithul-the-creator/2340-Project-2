from django.conf import settings
from django.db import models


class WorkModel(models.TextChoices):
    ONSITE = 'ONSITE', 'On-site'
    HYBRID = 'HYBRID', 'Hybrid'
    REMOTE = 'REMOTE', 'Remote'


class EmploymentType(models.TextChoices):
    FULL_TIME = 'FULL_TIME', 'Full-time'
    PART_TIME = 'PART_TIME', 'Part-time'
    INTERNSHIP = 'INTERNSHIP', 'Internship'
    CONTRACT = 'CONTRACT', 'Contract'


class SalaryUnit(models.TextChoices):
    HOURLY = 'HOURLY', 'Hourly'
    ANNUAL = 'ANNUAL', 'Annual'


class VisaSponsorship(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    NOT_AVAILABLE = 'NOT_AVAILABLE', 'No'
    NOT_PROVIDED = 'NOT_PROVIDED', 'Not provided'


class JobStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ACTIVE = 'ACTIVE', 'Active'
    PAUSED = 'PAUSED', 'Paused'


class ApplicationStatus(models.TextChoices):
    APPLIED = 'APPLIED', 'Applied'
    REVIEW = 'REVIEW', 'Review'
    INTERVIEW = 'INTERVIEW', 'Interview'
    OFFER = 'OFFER', 'Offer'
    CLOSED = 'CLOSED', 'Closed'


class Job(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    work_model = models.CharField(
        max_length=20, choices=WorkModel.choices, default=WorkModel.ONSITE
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
    )
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    skills = models.ManyToManyField(
        'accounts.Skill', blank=True, related_name='jobs'
    )
    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_max = models.PositiveIntegerField(blank=True, null=True)
    salary_unit = models.CharField(
        max_length=10, choices=SalaryUnit.choices, default=SalaryUnit.ANNUAL
    )
    visa_sponsorship = models.CharField(
        max_length=20,
        choices=VisaSponsorship.choices,
        default=VisaSponsorship.NOT_PROVIDED,
    )
    status = models.CharField(
        max_length=20, choices=JobStatus.choices, default=JobStatus.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.title} at {self.company}'

    @property
    def applicant_count(self):
        return self.applications.count()


class Application(models.Model):
    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='applications'
    )
    note = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = [('seeker', 'job')]

    def __str__(self):
        return f'{self.seeker} → {self.job} ({self.status})'


class DismissedRecommendation(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='dismissed_recommendations'
    )
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='dismissed_recommendations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('job', 'profile')]

    def __str__(self):
        return f'{self.profile} dismissed for {self.job}'


class SavedSearch(models.Model):
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_searches',
    )
    name = models.CharField(max_length=120)
    filters = models.JSONField(default=dict, blank=True)
    notify_email = models.BooleanField(default=False)
    notify_in_app = models.BooleanField(default=True)
    seen_profile_ids = models.JSONField(default=list, blank=True)
    last_notified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    notification_type = models.CharField(max_length=40, default='info')
    message = models.CharField(max_length=300)
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message
