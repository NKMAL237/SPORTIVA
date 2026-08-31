from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from organizations.models import SportsCategory
from events.models import EventCategory, Event, EventAttendance


class EventsUnitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='event_organizer',
            email='organizer@example.com',
            password='Password123!',
            role=User.Role.ORGANIZATION,
        )
        self.sport = SportsCategory.objects.create(name='Basketball', icon_class='fa-basketball')
        self.category = EventCategory.objects.create(name='Tournament')
        self.event = Event.objects.create(
            title='Yaoundé Street Basketball Cup',
            organizer=self.user,
            category=self.category,
            sport=self.sport,
            city='Yaoundé',
            venue_name='Palais des Sports',
            start_date=timezone.now() + timedelta(days=5),
            description='Annual 3x3 Basketball competition in Yaoundé.',
            entry_fee='Free',
            contact_whatsapp='+237677112233',
        )

    def test_event_creation(self):
        self.assertEqual(self.event.title, 'Yaoundé Street Basketball Cup')
        self.assertEqual(self.event.clean_whatsapp(), '237677112233')

    def test_events_list_view(self):
        response = self.client.get(reverse('events_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yaoundé Street Basketball Cup')

    def test_event_detail_view(self):
        response = self.client.get(reverse('event_detail', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

    def test_event_rsvp_action(self):
        self.client.login(username='event_organizer', password='Password123!')
        response = self.client.post(reverse('event_rsvp', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EventAttendance.objects.filter(event=self.event, user=self.user).exists())
