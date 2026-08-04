from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from organizations.models import SportsCategory, OrganizationProfile
from events.models import EventCategory, Event


class Command(BaseCommand):
    help = "Seeds realistic Cameroonian sports data for Sportiva CM"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Cameroonian sports data..."))

        # 1. Create Sports Categories
        sports = [
            ("Football", "fa-futbol", "Soccer leagues, youth academies, and local club tournaments."),
            ("Basketball", "fa-basketball", "Indoor and streetball 3x3 basketball competitions."),
            ("Athletics", "fa-person-running", "Track and field, marathon races, and sprinting clinics."),
            ("Combat Sports", "fa-hand-fist", "Judo, Karate, Boxing, and traditional wrestling (Lutte)."),
            ("Volleyball", "fa-volleyball", "Beach volleyball and court volleyball leagues."),
            ("Fitness & Gym", "fa-dumbbell", "Bodybuilding, crossfit, and community fitness workshops."),
        ]

        sport_objs = {}
        for name, icon, desc in sports:
            obj, _ = SportsCategory.objects.get_or_create(
                name=name,
                defaults={'icon_class': icon, 'description': desc}
            )
            sport_objs[name] = obj
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(sport_objs)} Sports Categories."))

        # 2. Create Event Categories
        event_cats = [
            ("Tournament", "fa-trophy"),
            ("Friendly Match", "fa-handshake"),
            ("Marathon / Road Race", "fa-person-running"),
            ("Training Camp", "fa-campground"),
            ("Fitness Workshop", "fa-heart-pulse"),
        ]

        event_cat_objs = {}
        for name, icon in event_cats:
            obj, _ = EventCategory.objects.get_or_create(
                name=name,
                defaults={'icon_class': icon}
            )
            event_cat_objs[name] = obj
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(event_cat_objs)} Event Categories."))

        # 3. Create Admin / Organizer User if missing
        organizer, created = User.objects.get_or_create(
            username='camer_admin',
            defaults={
                'email': 'admin@sportiva.cm',
                'role': User.Role.ORGANIZATION,
                'city': 'Yaoundé',
                'phone_number': '+237699000000',
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            organizer.set_password('Admin237!')
            organizer.save()
            self.stdout.write(self.style.SUCCESS("Created admin user 'camer_admin' (Password: Admin237!)"))

        # 4. Create Sample Organizations across Cameroon
        orgs_data = [
            {
                'username': 'canon_admin',
                'name': 'Canon Yaoundé Youth Academy',
                'category': sport_objs['Football'],
                'city': 'Yaoundé',
                'address': 'Quartier Mfinda, Near Stade Ahmadou Ahidjo',
                'lat': 3.8864,
                'lng': 11.5367,
                'desc': 'Premier youth football academy in Yaoundé focused on technical development and scouting.',
                'phone': '+237699000001',
                'whatsapp': '+237699000001',
                'email': 'canon.academy@sportiva.cm',
                'verified': True
            },
            {
                'username': 'douala_admin',
                'name': 'Douala Basketball Titans',
                'category': sport_objs['Basketball'],
                'city': 'Douala',
                'address': 'Akwa Boulevard, Douala',
                'lat': 4.0200,
                'lng': 9.8333,
                'desc': 'Competitive basketball club for youth and senior teams in Douala.',
                'phone': '+237699000002',
                'whatsapp': '+237699000002',
                'email': 'titans.douala@sportiva.cm',
                'verified': True
            },
            {
                'username': 'bafoussam_admin',
                'name': 'Highlands Athletics Bafoussam',
                'category': sport_objs['Athletics'],
                'city': 'Bafoussam',
                'address': 'Highland Stadium Road, Bafoussam',
                'lat': 5.4778,
                'lng': 10.4178,
                'desc': 'High-altitude endurance and track training for marathon runners.',
                'phone': '+237699000003',
                'whatsapp': '+237699000003',
                'email': 'athletics.bafoussam@sportiva.cm',
                'verified': False
            },
            {
                'username': 'garoua_admin',
                'name': 'Garoua Sahel Combat Club',
                'category': sport_objs['Combat Sports'],
                'city': 'Garoua',
                'address': 'Roumdé Adjia Complex, Garoua',
                'lat': 9.3000,
                'lng': 13.4000,
                'desc': 'Judo and traditional wrestling club developing champions in northern Cameroon.',
                'phone': '+237699000004',
                'whatsapp': '+237699000004',
                'email': 'combat.garoua@sportiva.cm',
                'verified': True
            },
        ]

        org_objs = []
        for o in orgs_data:
            mgr_user, _ = User.objects.get_or_create(
                username=o['username'],
                defaults={
                    'email': o['email'],
                    'role': User.Role.ORGANIZATION,
                    'city': o['city'],
                    'phone_number': o['phone'],
                    'is_verified': o['verified']
                }
            )
            org, _ = OrganizationProfile.objects.get_or_create(
                name=o['name'],
                defaults={
                    'user': mgr_user,
                    'sports_category': o['category'],
                    'city': o['city'],
                    'address': o['address'],
                    'latitude': o['lat'],
                    'longitude': o['lng'],
                    'description': o['desc'],
                    'phone_number': o['phone'],
                    'whatsapp_number': o['whatsapp'],
                    'email': o['email'],
                    'is_verified': o['verified']
                }
            )
            org_objs.append(org)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(org_objs)} Organizations."))

        # 5. Create Sample Events
        now = timezone.now()
        events_data = [
            {
                'title': 'Coupe Inter-Quartiers Yaoundé 2026',
                'category': event_cat_objs['Tournament'],
                'sport': sport_objs['Football'],
                'organization': org_objs[0],
                'city': 'Yaoundé',
                'venue': 'Stade Annexe 1 Ahmadou Ahidjo',
                'lat': 3.8864,
                'lng': 11.5367,
                'start': now + timedelta(days=12),
                'desc': 'Annual inter-neighborhood football championship bringing together 16 top local teams.',
                'whatsapp': '+237699000001',
                'fee': 'Free Entry',
            },
            {
                'title': 'Grand Marathon de Douala',
                'category': event_cat_objs['Marathon / Road Race'],
                'sport': sport_objs['Athletics'],
                'organization': org_objs[1],
                'city': 'Douala',
                'venue': 'Akwa Boulevard, Douala',
                'lat': 4.0200,
                'lng': 9.8333,
                'start': now + timedelta(days=25),
                'desc': '21km half-marathon open to amateur and professional runners across Central Africa.',
                'whatsapp': '+237699000002',
                'fee': '2,000 FCFA',
            },
            {
                'title': 'Open 3x3 Street Basketball Bafoussam',
                'category': event_cat_objs['Tournament'],
                'sport': sport_objs['Basketball'],
                'organization': org_objs[2],
                'city': 'Bafoussam',
                'venue': 'Palais des Sports Bafoussam',
                'lat': 5.4778,
                'lng': 10.4178,
                'start': now + timedelta(days=35),
                'desc': 'Fast-paced 3-on-3 outdoor street basketball tournament with cash prizes.',
                'whatsapp': '+237699000003',
                'fee': '1,000 FCFA / Team',
            },
        ]

        event_count = 0
        for e in events_data:
            ev, created = Event.objects.get_or_create(
                title=e['title'],
                defaults={
                    'organizer': organizer,
                    'organization': e['organization'],
                    'category': e['category'],
                    'sport': e['sport'],
                    'city': e['city'],
                    'venue_name': e['venue'],
                    'latitude': e['lat'],
                    'longitude': e['lng'],
                    'start_date': e['start'],
                    'description': e['desc'],
                    'contact_whatsapp': e['whatsapp'],
                    'entry_fee': e['fee'],
                    'is_published': True
                }
            )
            if created:
                event_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {event_count} Events."))
        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
