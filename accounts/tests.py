from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class AccountsUnitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='athlete_user',
            email='athlete@example.com',
            password='Password123!',
            role=User.Role.ATHLETE,
            city='Douala',
        )

    def test_custom_user_creation_and_roles(self):
        self.assertEqual(self.user.username, 'athlete_user')
        self.assertEqual(self.user.role, User.Role.ATHLETE)
        self.assertEqual(self.user.city, 'Douala')
        self.assertTrue(self.user.check_password('Password123!'))

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_success(self):
        login_successful = self.client.login(username='athlete_user', password='Password123!')
        self.assertTrue(login_successful)

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)