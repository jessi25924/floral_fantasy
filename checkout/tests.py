from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from checkout.models import Order
from decimal import Decimal
from unittest.mock import patch
import json


class CheckoutTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='password')

        # Product and Category
        self.category = Category.objects.create(name='Test Category', display_name='Test Cat')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Description',
            price=Decimal('10.00'),
            in_stock=True
        )

        #cart session
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

    def test_checkout_page_loads(self):
        """Checkout page loads for non-empty cart"""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Checkout')

    def test_discount_code_applied(self):
        response = self.client.post(reverse('checkout'), {'discount_code': 'SUMMER10'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('discount_amount', response.context)

    def test_checkout_success_page(self):
        order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Street',
            town_or_city='Town',
            country='US',
            delivery_cost=2.99,
            order_total=Decimal('20.00'),
            grand_total=Decimal('22.99')
        )
        response = self.client.get(reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)


class WebhookTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("webhook")
        self.payload = json.dumps({"type": "payment_intent.succeeded"}).encode()
        self.headers = {"HTTP_STRIPE_SIGNATURE": "test"}

    @patch("checkout.webhooks.stripe.Webhook.construct_event")
    def test_webhook_succeeded(self, mock_event):
        mock_event.return_value = {"type": "payment_intent.succeeded"}
        r = self.client.post(self.url, self.payload, content_type="application/json", **self.headers)
        self.assertContains(r, "payment_intent.succeeded")

    @patch("checkout.webhooks.stripe.Webhook.construct_event", side_effect=ValueError)
    def test_invalid_payload(self, _):
        r = self.client.post(self.url, "bad", content_type="application/json", **self.headers)
        self.assertEqual(r.status_code, 400)
