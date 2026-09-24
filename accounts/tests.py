from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import AccountStatus, Privacy, Profile, Role, Skill
from jobs.models import Application, ApplicationStatus, Job, JobStatus, SavedSearch
from jobs.services import recommend_candidates_for_job, visible_seeker_queryset


class SeekrCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.seeker = User.objects.create_user(
            username='seeker1', password='testpass123', email='s@example.com'
        )
        self.seeker_profile = Profile.objects.get(user=self.seeker)
        self.seeker_profile.role = Role.SEEKER
        self.seeker_profile.headline = 'CS student'
        self.seeker_profile.location = 'Atlanta'
        self.seeker_profile.privacy = Privacy.PUBLIC_RECRUITERS
        self.seeker_profile.save()
        python, _ = Skill.objects.get_or_create(name='Python')
        self.seeker_profile.skills.add(python)

        self.recruiter = User.objects.create_user(
            username='recruiter1', password='testpass123', email='r@example.com'
        )
        self.recruiter_profile = Profile.objects.get(user=self.recruiter)
        self.recruiter_profile.role = Role.RECRUITER
        self.recruiter_profile.company = 'Acme'
        self.recruiter_profile.save()

        self.admin = User.objects.create_user(
            username='admin1', password='testpass123', is_staff=True
        )
        self.admin_profile = Profile.objects.get(user=self.admin)
        self.admin_profile.role = Role.ADMIN
        self.admin_profile.save()

        self.job = Job.objects.create(
            owner=self.recruiter,
            title='Backend Intern',
            company='Acme',
            location='Atlanta',
            description='Build APIs',
            status=JobStatus.ACTIVE,
        )
        self.job.skills.add(python)

    def test_signup_assigns_role(self):
        response = self.client.post(
            reverse('accounts.signup'),
            {
                'username': 'newseeker',
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!',
                'role': Role.SEEKER,
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newseeker')
        self.assertEqual(user.profile.role, Role.SEEKER)

    def test_suspended_user_cannot_login(self):
        self.seeker_profile.status = AccountStatus.SUSPENDED
        self.seeker_profile.save()
        response = self.client.post(
            reverse('accounts.login'),
            {'username': 'seeker1', 'password': 'testpass123'},
        )
        self.assertContains(response, 'suspended')

    def test_privacy_hides_private_profiles(self):
        self.seeker_profile.privacy = Privacy.PRIVATE
        self.seeker_profile.save()
        qs = visible_seeker_queryset(self.recruiter)
        self.assertFalse(qs.filter(pk=self.seeker_profile.pk).exists())

    def test_applications_only_visible_after_apply(self):
        self.seeker_profile.privacy = Privacy.APPLICATIONS_ONLY
        self.seeker_profile.save()
        qs = visible_seeker_queryset(self.recruiter)
        self.assertFalse(qs.filter(pk=self.seeker_profile.pk).exists())

        Application.objects.create(seeker=self.seeker, job=self.job)
        qs = visible_seeker_queryset(self.recruiter)
        self.assertTrue(qs.filter(pk=self.seeker_profile.pk).exists())

    def test_seeker_can_apply_once(self):
        self.client.login(username='seeker1', password='testpass123')
        url = reverse('jobs.apply', args=[self.job.pk])
        response = self.client.post(url, {'note': 'Excited to join'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Application.objects.filter(seeker=self.seeker, job=self.job).count(), 1)

        response = self.client.post(url, {'note': 'Again'})
        self.assertEqual(Application.objects.filter(seeker=self.seeker, job=self.job).count(), 1)

    def test_recruiter_can_update_application_status(self):
        app = Application.objects.create(seeker=self.seeker, job=self.job)
        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.post(
            reverse('jobs.applicants', args=[self.job.pk]) + f'?app={app.pk}',
            {'status': ApplicationStatus.REVIEW},
        )
        self.assertEqual(response.status_code, 302)
        app.refresh_from_db()
        self.assertEqual(app.status, ApplicationStatus.REVIEW)

    def test_job_search_filters(self):
        response = self.client.get(reverse('jobs.list'), {'q': 'Backend', 'location': 'Atlanta'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Backend Intern')

    def test_recommendations_include_skill_reason(self):
        results = recommend_candidates_for_job(self.job)
        self.assertTrue(results)
        self.assertEqual(results[0]['profile'], self.seeker_profile)
        self.assertTrue(any('Python' in r for r in results[0]['reasons']))

    def test_admin_can_suspend_user(self):
        self.client.login(username='admin1', password='testpass123')
        response = self.client.post(
            reverse('accounts.manage_user_detail', args=[self.seeker.id]),
            {'role': Role.SEEKER, 'status': AccountStatus.SUSPENDED},
        )
        self.assertEqual(response.status_code, 302)
        self.seeker_profile.refresh_from_db()
        self.assertEqual(self.seeker_profile.status, AccountStatus.SUSPENDED)

    def test_recruiter_job_create_and_saved_search(self):
        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.post(
            reverse('jobs.recruiter_job_create'),
            {
                'title': 'Frontend Intern',
                'company': 'Acme',
                'location': 'Remote',
                'work_model': 'REMOTE',
                'employment_type': 'INTERNSHIP',
                'description': 'Build UI',
                'responsibilities': '',
                'qualifications': '',
                'salary_min': '',
                'salary_max': '',
                'salary_unit': 'ANNUAL',
                'visa_sponsorship': 'NOT_PROVIDED',
                'status': JobStatus.ACTIVE,
                'skills_text': 'React',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Job.objects.filter(title='Frontend Intern').exists())

        response = self.client.post(
            reverse('jobs.saved_search_create') + '?skills=Python&location=Atlanta',
            {
                'name': 'Python in Atlanta',
                'notify_in_app': True,
                'notify_email': False,
            },
        )
        self.assertEqual(response.status_code, 302)
        search = SavedSearch.objects.get(name='Python in Atlanta')
        self.assertEqual(search.filters.get('skills'), 'Python')

    def test_role_gates_recruiter_pages(self):
        self.client.login(username='seeker1', password='testpass123')
        response = self.client.get(reverse('jobs.recruiter_jobs'))
        self.assertEqual(response.status_code, 302)
