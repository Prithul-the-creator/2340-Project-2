from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from accounts.models import Education, Privacy, Profile, Project, Role, Skill
from jobs.models import Job, JobStatus, WorkModel


class Command(BaseCommand):
    help = 'Seed demo Seekr users, profiles, and jobs'

    def handle(self, *args, **options):
        python, _ = Skill.objects.get_or_create(name='Python')
        react, _ = Skill.objects.get_or_create(name='React')
        sql, _ = Skill.objects.get_or_create(name='SQL')

        seeker, created = User.objects.get_or_create(
            username='seeker',
            defaults={'email': 'seeker@seekr.local', 'first_name': 'Alex', 'last_name': 'Chen'},
        )
        if created:
            seeker.set_password('seeker123')
            seeker.save()
        profile = Profile.objects.get(user=seeker)
        profile.role = Role.SEEKER
        profile.headline = 'Computer Science @ Georgia Tech'
        profile.bio = 'Interested in distributed systems and developer infrastructure.'
        profile.location = 'Atlanta, GA'
        profile.privacy = Privacy.PUBLIC_RECRUITERS
        profile.save()
        profile.skills.set([python, sql])
        if not profile.educations.exists():
            Education.objects.create(
                profile=profile,
                school='Georgia Tech',
                degree='BS',
                field='Computer Science',
                graduation_year=2026,
            )
        if not profile.projects.exists():
            project = Project.objects.create(
                profile=profile,
                name='Campus Course Planner',
                description='Helps students plan degree paths.',
            )
            project.skills.add(python, react)

        recruiter, created = User.objects.get_or_create(
            username='recruiter',
            defaults={'email': 'recruiter@seekr.local', 'first_name': 'Jordan', 'last_name': 'Lee'},
        )
        if created:
            recruiter.set_password('recruiter123')
            recruiter.save()
        rprofile = Profile.objects.get(user=recruiter)
        rprofile.role = Role.RECRUITER
        rprofile.company = 'Northstar Labs'
        rprofile.headline = 'University recruiting'
        rprofile.save()

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@seekr.local',
                'first_name': 'Sam',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        aprofile = Profile.objects.get(user=admin)
        aprofile.role = Role.ADMIN
        aprofile.save()

        if not Job.objects.filter(title='Software Engineering Intern').exists():
            job = Job.objects.create(
                owner=recruiter,
                title='Software Engineering Intern',
                company='Northstar Labs',
                location='Atlanta, GA',
                work_model=WorkModel.HYBRID,
                description='Join our early-career engineering cohort.',
                responsibilities='Ship features with a mentor.\nWrite tests and docs.',
                qualifications='Python or JavaScript experience preferred.',
                salary_min=25,
                salary_max=35,
                salary_unit='HOURLY',
                visa_sponsorship='AVAILABLE',
                status=JobStatus.ACTIVE,
            )
            job.skills.add(python, react)

        self.stdout.write(self.style.SUCCESS(
            'Demo users ready:\n'
            '  seeker / seeker123\n'
            '  recruiter / recruiter123\n'
            '  admin / admin123'
        ))
