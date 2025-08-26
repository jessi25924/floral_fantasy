from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from checkout.models import Order


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password'
        )
        self.profile = self.user.userprofile

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile")

    def test_profile_update(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '1234567890',
            'default_town_or_city': 'Test City',
        })
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.default_phone_number, '1234567890')

    def test_order_history_view(self):
        order = Order.objects.create(
            order_number="ORDER123",
            full_name="Test User",
            email="test@example.com",
        )
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('order_history', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)
