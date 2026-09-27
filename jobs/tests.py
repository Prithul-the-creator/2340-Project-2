from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Application, Job


class JobApplicationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='seeker', password='test-pass')
        self.job = Job.objects.create(
            title='Junior Developer',
            company='Seekr',
            skills_needed='Python',
            remote_work=True,
        )

    def test_job_listing_renders_current_job_fields(self):
        response = self.client.get(reverse('jobs.index'))

        self.assertContains(response, 'Junior Developer')
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Remote')

    def test_seeker_applies_with_a_note(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('jobs.apply', args=[self.job.pk]), {
            'note': 'I am excited to bring my Python experience to this role.',
        })

        self.assertRedirects(response, reverse('jobs.applications'))
        application = Application.objects.get(user=self.user, job=self.job)
        self.assertEqual(application.note, 'I am excited to bring my Python experience to this role.')
        self.assertContains(self.client.get(reverse('jobs.applications')), application.note)

    def test_seeker_cannot_apply_to_the_same_job_twice(self):
        self.client.force_login(self.user)
        apply_url = reverse('jobs.apply', args=[self.job.pk])
        self.client.post(apply_url, {'note': 'First note'})
        self.client.post(apply_url, {'note': 'Second note'})

        self.assertEqual(Application.objects.filter(user=self.user, job=self.job).count(), 1)
        self.assertEqual(Application.objects.get(user=self.user, job=self.job).note, 'First note')

    def test_application_requires_a_note(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('jobs.apply', args=[self.job.pk]), {}, follow=True)

        self.assertContains(response, 'Please add a note')
        self.assertFalse(Application.objects.exists())

    def test_applying_requires_login(self):
        response = self.client.post(reverse('jobs.apply', args=[self.job.pk]), {'note': 'A note'})

        self.assertRedirects(response, f"{reverse('accounts.login')}?next={reverse('jobs.apply', args=[self.job.pk])}")
        self.assertFalse(Application.objects.exists())

    def test_application_status_defaults_to_applied(self):
        application = Application.objects.create(user=self.user, job=self.job, note='Looking forward to this role.')

        self.assertEqual(application.status, Application.Status.APPLIED)

    def test_seeker_can_update_application_status(self):
        application = Application.objects.create(user=self.user, job=self.job, note='Looking forward to this role.')
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('jobs.update_application_status', args=[application.pk]),
            {'status': Application.Status.INTERVIEW},
        )

        self.assertRedirects(response, reverse('jobs.applications'))
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.INTERVIEW)
        self.assertContains(self.client.get(reverse('jobs.applications')), 'Interview')

    def test_seeker_cannot_update_another_users_application(self):
        other_user = get_user_model().objects.create_user(username='other-seeker', password='test-pass')
        application = Application.objects.create(user=other_user, job=self.job, note='Another seeker note.')
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('jobs.update_application_status', args=[application.pk]),
            {'status': Application.Status.OFFER},
        )

        self.assertEqual(response.status_code, 404)
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.APPLIED)

    def test_invalid_application_status_is_rejected(self):
        application = Application.objects.create(user=self.user, job=self.job, note='Looking forward to this role.')
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('jobs.update_application_status', args=[application.pk]),
            {'status': 'not-a-status'},
            follow=True,
        )

        self.assertContains(response, 'Choose a valid application status.')
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.APPLIED)
