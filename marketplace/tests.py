from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from marketplace.models import Product, ProductCategory


class MarketplaceFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='selleruser',
            email='seller@example.com',
            password='strongpass123',
            role=User.Role.ORGANIZATION,
        )
        self.category = ProductCategory.objects.create(name='Football Boots')
        self.product = Product.objects.create(
            seller=self.user,
            category=self.category,
            title='Nike Football Boots',
            description='Excellent condition boots for training and matches.',
            price=25000,
            condition='GOOD',
            city='Yaoundé',
            whatsapp_number='+237699000111',
        )

    def test_marketplace_list_page_loads(self):
        response = self.client.get(reverse('marketplace_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_loads(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)

    def test_product_create_requires_login(self):
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_product_create_post(self):
        self.client.login(username='selleruser', password='strongpass123')
        response = self.client.post(reverse('product_create'), {
            'title': 'Adidas Shin Guards',
            'category': self.category.pk,
            'description': 'Lightweight protective guards.',
            'price': 5000,
            'condition': 'NEW',
            'city': 'Douala',
            'whatsapp_number': '+237699000222',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(title='Adidas Shin Guards').exists())