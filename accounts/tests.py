from importlib import import_module

from django.apps import apps
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import (
    AccountStatus,
    Education,
    Experience,
    Link,
    Privacy,
    Profile,
    Project,
    Role,
    Skill,
)
from jobs.models import (
    Application,
    ApplicationStatus,
    DismissedRecommendation,
    Job,
    JobStatus,
    Notification,
    SavedSearch,
)
from jobs.services import (
    check_saved_searches_for_profile,
    recommend_candidates_for_job,
    visible_seeker_queryset,
)


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

    def _make_seeker(self, username, skill_names, location='Atlanta'):
        user = User.objects.create_user(username=username, password='testpass123')
        profile = Profile.objects.get(user=user)
        profile.location = location
        profile.save()
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            profile.skills.add(skill)
        return profile

    def _save_search(self, query, name='Search'):
        self.client.login(username='recruiter1', password='testpass123')
        self.client.post(
            reverse('jobs.saved_search_create') + query,
            {'name': name, 'notify_in_app': True},
        )
        return SavedSearch.objects.get(name=name)

    def test_saved_search_skips_existing_matches(self):
        search = self._save_search('?skills=Python')
        self.assertIn(self.seeker_profile.pk, search.seen_profile_ids)

        check_saved_searches_for_profile(self.seeker_profile)
        self.assertFalse(
            Notification.objects.filter(
                user=self.recruiter, notification_type='saved_search'
            ).exists()
        )

    def test_saved_search_alerts_new_match_once(self):
        self._save_search('?skills=Python')
        newcomer = self._make_seeker('newcomer', ['Python'])

        check_saved_searches_for_profile(newcomer)
        check_saved_searches_for_profile(newcomer)
        alerts = Notification.objects.filter(
            user=self.recruiter, notification_type='saved_search'
        )
        self.assertEqual(alerts.count(), 1)
        self.assertEqual(alerts.first().link, f'/candidates/{newcomer.pk}/')

    def test_education_add_triggers_saved_search(self):
        self._save_search('?school=Georgia+Tech')
        self.client.login(username='seeker1', password='testpass123')
        self.client.post(
            reverse('accounts.education_add'),
            {'school': 'Georgia Tech', 'degree': 'BS', 'field': '', 'graduation_year': 2027},
        )
        self.assertTrue(
            Notification.objects.filter(
                user=self.recruiter, notification_type='saved_search'
            ).exists()
        )

    def test_saved_search_run_encodes_filters(self):
        search = self._save_search('?skills=C%2B%2B')
        response = self.client.get(reverse('jobs.saved_search_run', args=[search.pk]))
        self.assertEqual(response['Location'], '/candidates/?skills=C%2B%2B')

    def test_saved_search_edit_updates_alerts(self):
        search = self._save_search('?skills=Python')
        self.client.post(
            reverse('jobs.saved_search_edit', args=[search.pk]),
            {'name': 'Renamed', 'notify_email': True},
        )
        search.refresh_from_db()
        self.assertEqual(search.name, 'Renamed')
        self.assertTrue(search.notify_email)
        self.assertFalse(search.notify_in_app)

    def test_recommendations_ignore_skill_case(self):
        self.seeker_profile.skills.clear()
        lower, _ = Skill.objects.get_or_create(name='python')
        self.seeker_profile.skills.add(lower)
        results = recommend_candidates_for_job(self.job)
        self.assertEqual(results[0]['profile'], self.seeker_profile)
        self.assertIn('Has 1 of 1 required skills: Python', results[0]['reasons'])

    def test_recommendations_skip_location_for_remote_jobs(self):
        self.job.work_model = 'REMOTE'
        self.job.save()
        results = recommend_candidates_for_job(self.job)
        self.assertFalse(any('Located' in r for r in results[0]['reasons']))

    def test_invite_candidate_notifies_once(self):
        self.client.login(username='recruiter1', password='testpass123')
        url = reverse('jobs.invite_candidate', args=[self.job.pk, self.seeker_profile.pk])
        self.client.post(url)
        self.client.post(url)
        invites = Notification.objects.filter(user=self.seeker, notification_type='invite')
        self.assertEqual(invites.count(), 1)

        response = self.client.get(reverse('jobs.applicants', args=[self.job.pk]))
        self.assertContains(response, 'Invited')

    def test_invite_requires_active_job(self):
        self.job.status = JobStatus.DRAFT
        self.job.save()
        self.client.login(username='recruiter1', password='testpass123')
        self.client.post(
            reverse('jobs.invite_candidate', args=[self.job.pk, self.seeker_profile.pk])
        )
        self.assertFalse(Notification.objects.filter(notification_type='invite').exists())

    def test_saved_searches_page_shows_labels_and_matches(self):
        self._save_search('?skills=Python&graduation_year=2027')
        response = self.client.get(reverse('jobs.saved_searches'))
        self.assertContains(response, 'Graduation year: 2027')
        self.assertContains(response, '0 matches')

    def test_skill_text_reuses_existing_capitalization(self):
        self.client.login(username='seeker1', password='testpass123')
        self.client.post(
            reverse('accounts.profile_edit'),
            {'headline': 'CS student', 'skills_text': 'python, PYTHON, Go'},
        )
        self.assertEqual(Skill.objects.filter(name__iexact='python').count(), 1)
        self.assertEqual(
            sorted(self.seeker_profile.skills.values_list('name', flat=True)),
            ['Go', 'Python'],
        )

    def test_merge_duplicate_skills_migration(self):
        duplicate = Skill.objects.create(name='python')
        self.job.skills.add(duplicate)
        migration = import_module('accounts.migrations.0002_merge_duplicate_skills')
        migration.merge_duplicate_skills(apps, None)

        self.assertFalse(Skill.objects.filter(name='python').exists())
        self.assertEqual(list(self.job.skills.values_list('name', flat=True)), ['Python'])

    def test_candidate_relevance_ranks_project_evidence_first(self):
        newcomer = self._make_seeker('newcomer', ['Python'])
        project = Project.objects.create(profile=newcomer, name='Scraper')
        project.skills.add(Skill.objects.get(name='Python'))
        self.seeker_profile.save()

        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.get(reverse('jobs.candidates'), {'skills': 'Python'})
        content = response.content.decode()
        self.assertLess(content.index('newcomer'), content.index('seeker1'))

        response = self.client.get(
            reverse('jobs.candidates'), {'skills': 'Python', 'sort': 'updated'}
        )
        content = response.content.decode()
        self.assertLess(content.index('seeker1'), content.index('newcomer'))
        self.assertContains(response, '2 candidates')

    def test_dismissed_recommendation_is_hidden_until_restored(self):
        self.client.login(username='recruiter1', password='testpass123')
        self.client.post(
            reverse('jobs.dismiss_recommendation', args=[self.job.pk, self.seeker_profile.pk])
        )
        self.assertTrue(DismissedRecommendation.objects.filter(job=self.job).exists())
        self.assertEqual(recommend_candidates_for_job(self.job), [])

        response = self.client.get(reverse('jobs.applicants', args=[self.job.pk]))
        self.assertContains(response, '1 dismissed')

        self.client.post(reverse('jobs.restore_recommendations', args=[self.job.pk]))
        self.assertEqual(
            recommend_candidates_for_job(self.job)[0]['profile'], self.seeker_profile
        )

    def _apply_with_full_profile(self):
        Education.objects.create(profile=self.seeker_profile, school='Georgia Tech')
        Experience.objects.create(
            profile=self.seeker_profile, title='SWE Intern', company='Initech'
        )
        Project.objects.create(profile=self.seeker_profile, name='Course Planner')
        Link.objects.create(
            profile=self.seeker_profile, link_type='GITHUB', url='https://github.com/seeker1'
        )
        return Application.objects.create(
            seeker=self.seeker, job=self.job, note='Built APIs at Initech'
        )

    def test_applicant_panel_shows_profile_and_application(self):
        app = self._apply_with_full_profile()
        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.get(
            reverse('jobs.applicants', args=[self.job.pk]), {'app': app.pk}
        )
        for text in [
            'Built APIs at Initech',
            'Georgia Tech',
            'SWE Intern',
            'Course Planner',
            'https://github.com/seeker1',
        ]:
            self.assertContains(response, text)

    def test_applicant_panel_respects_private_profile(self):
        app = self._apply_with_full_profile()
        self.seeker_profile.privacy = Privacy.PRIVATE
        self.seeker_profile.save()
        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.get(
            reverse('jobs.applicants', args=[self.job.pk]), {'app': app.pk}
        )
        self.assertContains(response, 'Built APIs at Initech')
        self.assertContains(response, 'profile is private')
        self.assertNotContains(response, 'Georgia Tech')

    def test_candidate_detail_shows_links(self):
        self._apply_with_full_profile()
        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.get(
            reverse('jobs.candidate_detail', args=[self.seeker_profile.pk])
        )
        self.assertContains(response, 'https://github.com/seeker1')
