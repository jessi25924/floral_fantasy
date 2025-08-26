from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from products.models import Product


class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
            in_stock=True
        )

    def test_add_update_remove_cart(self):
        # Add product to cart
        self.client.post(reverse('add_to_cart', args=[self.product.id]), {'quantity': 2, 'redirect_url': '/'})
        cart = self.client.session['cart']
        self.assertEqual(cart[str(self.product.id)], 2)

        # Update product quantity
        self.client.post(reverse('update_cart', args=[self.product.id]), {'quantity': 5, 'redirect_url': '/'})
        cart = self.client.session['cart']
        self.assertEqual(cart[str(self.product.id)], 5)

        # Remove product
        self.client.post(reverse('remove_from_cart', args=[self.product.id]), {'redirect_url': '/'})
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)

    def test_view_cart(self):
        # cart empty
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
