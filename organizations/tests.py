from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from organizations.models import SportsCategory, OrganizationProfile


class OrganizationsUnitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='org_admin',
            email='org@example.com',
            password='Password123!',
            role=User.Role.ORGANIZATION,
        )
        self.category = SportsCategory.objects.create(name='Football', icon_class='fa-futbol')
        self.org = OrganizationProfile.objects.create(
            user=self.user,
            name='Yaoundé Football Academy',
            sports_category=self.category,
            city='Yaoundé',
            address='Omnisport',
            description='Leading youth football training academy.',
            whatsapp_number='+237699112233',
        )

    def test_organization_profile_creation(self):
        self.assertEqual(self.org.name, 'Yaoundé Football Academy')
        self.assertEqual(self.org.clean_whatsapp(), '237699112233')
        self.assertEqual(str(self.org), 'Yaoundé Football Academy (Yaoundé)')

    def test_organization_list_view(self):
        response = self.client.get(reverse('organizations_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yaoundé Football Academy')

    def test_organization_detail_view(self):
        response = self.client.get(reverse('organization_detail', args=[self.org.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.org.name)

    def test_organization_create_requires_login(self):
        response = self.client.get(reverse('organization_create'))
        self.assertEqual(response.status_code, 302)
