from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.TextChoices):
    SEEKER = 'SEEKER', 'Job Seeker'
    RECRUITER = 'RECRUITER', 'Recruiter'
    ADMIN = 'ADMIN', 'Administrator'


class Privacy(models.TextChoices):
    PUBLIC_RECRUITERS = 'PUBLIC_RECRUITERS', 'Public to recruiters'
    APPLICATIONS_ONLY = 'APPLICATIONS_ONLY', 'Applications only'
    PRIVATE = 'PRIVATE', 'Private'


class AccountStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    SUSPENDED = 'SUSPENDED', 'Suspended'


class Skill(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def skills_from_text(raw):
    # Reuse an existing skill whatever its capitalization so "python" and
    # "Python" stay one skill for search, filters, and recommendations.
    skills = []
    for name in [n.strip() for n in (raw or '').split(',') if n.strip()]:
        skill = Skill.objects.filter(name__iexact=name).first()
        if skill is None:
            skill = Skill.objects.create(name=name)
        if skill not in skills:
            skills.append(skill)
    return skills


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SEEKER,
    )
    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    privacy = models.CharField(
        max_length=30,
        choices=Privacy.choices,
        default=Privacy.PUBLIC_RECRUITERS,
    )
    company = models.CharField(max_length=120, blank=True)
    company_website = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.role})'

    @property
    def display_name(self):
        full = self.user.get_full_name().strip()
        return full or self.user.username

    def is_visible_to_recruiter(self, recruiter_user=None):
        if self.role != Role.SEEKER:
            return False
        if self.status != AccountStatus.ACTIVE:
            return False
        if self.privacy == Privacy.PRIVATE:
            return False
        if self.privacy == Privacy.PUBLIC_RECRUITERS:
            return True
        if self.privacy == Privacy.APPLICATIONS_ONLY and recruiter_user:
            return self.user.applications.filter(
                job__owner=recruiter_user
            ).exists()
        return False


class Education(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='educations'
    )
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=120, blank=True)
    field = models.CharField(max_length=120, blank=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-graduation_year', 'school']

    def __str__(self):
        return f'{self.school} — {self.degree}'


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='experiences'
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date', 'title']

    def __str__(self):
        return f'{self.title} at {self.company}'


class Project(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='projects'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='projects')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LinkType(models.TextChoices):
    WEBSITE = 'WEBSITE', 'Website'
    GITHUB = 'GITHUB', 'GitHub'
    LINKEDIN = 'LINKEDIN', 'LinkedIn'
    OTHER = 'OTHER', 'Other'


class Link(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='links'
    )
    link_type = models.CharField(
        max_length=20, choices=LinkType.choices, default=LinkType.OTHER
    )
    url = models.URLField()
    label = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.label or self.url


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        role = Role.ADMIN if instance.is_superuser else Role.SEEKER
        Profile.objects.get_or_create(user=instance, defaults={'role': role})
    elif instance.is_superuser:
        profile, _ = Profile.objects.get_or_create(user=instance)
        if profile.role != Role.ADMIN:
            profile.role = Role.ADMIN
            profile.save(update_fields=['role'])
