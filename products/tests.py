from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from decimal import Decimal


class ProductTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.admin = User.objects.create_superuser(username='admin', password='pass')
        self.category = Category.objects.create(name='Bouquet', display_name='Bouquet Display')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('19.99'),
            in_stock=True,
            category=self.category
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.description)

    def test_add_product_superuser(self):
        self.client.login(username='admin', password='pass')
        response = self.client.post(reverse('products:add_product'), {
            'name': 'New Product',
            'description': 'New Description',
            'price': '29.99',
            'category': self.category.id,
            'in_stock': True,
        })
        self.assertEqual(response.status_code, 302)  # Redirect to detail
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_add_product_non_user(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('products:add_product'))
        self.assertRedirects(response, reverse('landing'))

    def test_edit_product_superuser(self):
        self.client.login(username='admin', password='pass')
        response = self.client.post(reverse('products:edit_product', args=[self.product.id]), {
            'name': 'Edited Product',
            'description': self.product.description,
            'price': str(self.product.price),
            'category': self.category.id,
            'in_stock': self.product.in_stock,
        })
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Edited Product')

    def test_delete_product_superuser(self):
        self.client.login(username='admin', password='pass')
        response = self.client.post(reverse('products:delete_product', args=[self.product.id]))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        self.assertEqual(response.status_code, 302)
