from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core import mail


class LandingTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_loads(self):
        """Landing page loads successfully"""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_contact_submit_valid_post(self):
        """Contact form submits and sends email"""
        response = self.client.post(reverse('contact_submit'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Hello!',
        }, HTTP_REFERER='/')
        # Check redirect back to referer
        self.assertEqual(response.status_code, 302)
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('New contact form submission from Test User', mail.outbox[0].subject)

    def test_contact_submit_invalid_method(self):
        """GET to contact_submit should return 400"""
        response = self.client.get(reverse('contact_submit'))
        self.assertEqual(response.status_code, 400)

    def test_contact_submit_invalid_data(self):
        """POST with missing fields should redirect and show error"""
        response = self.client.post(reverse('contact_submit'), {
            'name': '',
            'email': 'invalid-email',
            'message': ''
        }, HTTP_REFERER='/')
        # Redirect back to referer
        self.assertEqual(response.status_code, 302)
        # No email should be sent
        self.assertEqual(len(mail.outbox), 0)
