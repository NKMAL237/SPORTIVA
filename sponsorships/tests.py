from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from sponsorships.models import Campaign, Pledge


class SponsorshipsFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='sponsoruser',
            email='sponsor@example.com',
            password='strongpass123',
            role=User.Role.SPONSOR,
        )
        self.campaign = Campaign.objects.create(
            creator=self.user,
            title='Road to National Finals',
            category='TRAVEL',
            description='Support the team travel fund.',
            target_amount=500000,
            raised_amount=200000,
            city='Yaoundé',
            whatsapp_number='+237699000000',
        )

    def test_sponsorships_list_page_loads(self):
        response = self.client.get(reverse('sponsorships_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sponsorship & Funding Campaigns')

    def test_campaign_detail_page_loads(self):
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)

    def test_campaign_create_requires_login(self):
        response = self.client.get(reverse('campaign_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_campaign_create_post(self):
        self.client.login(username='sponsoruser', password='strongpass123')
        response = self.client.post(reverse('campaign_create'), {
            'title': 'New Balls & Training Gear',
            'category': 'EQUIPMENT',
            'description': 'Equipment fund for youth academy.',
            'target_amount': 300000,
            'city': 'Douala',
            'whatsapp_number': '+237699333444',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Campaign.objects.filter(title='New Balls & Training Gear').exists())

    def test_pledge_post(self):
        self.client.login(username='sponsoruser', password='strongpass123')
        response = self.client.post(reverse('campaign_detail', args=[self.campaign.pk]), {
            'amount': 50000,
            'message': 'Good luck team!',
            'is_anonymous': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pledge.objects.filter(campaign=self.campaign, amount=50000).exists())
