from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, AthleteExploit, Follow
from organizations.models import SportsCategory, OrganizationProfile
from events.models import EventCategory, Event, EventRegistration
from sponsorships.models import SponsorProfile, SponsorshipRequest, SponsorshipContract, Campaign, Pledge
from media_feed.models import Post
from chat.models import Conversation, ChatMessage


class Command(BaseCommand):
    help = "Seeds comprehensive realistic global sports network data for SPORTIVA"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[INFO] Seeding SPORTIVA Global Sports Network data..."))

        # 1. Create Sports Categories
        sports = [
            ("Football", "fa-futbol", "Global football leagues, youth academies, and international scouting."),
            ("Basketball", "fa-basketball", "Indoor, collegiate, and streetball 3x3 basketball competitions."),
            ("Athletics", "fa-person-running", "Track and field, marathon races, sprinting, and Olympic clinics."),
            ("Tennis", "fa-baseball", "Grand Slam circuits, ATP/WTA qualifiers, and elite tennis clinics."),
            ("Combat Sports", "fa-hand-fist", "Boxing, Judo, MMA, and grappling championships worldwide."),
            ("Swimming & Aquatics", "fa-person-swimming", "Olympic pools, competitive swimming, and water sports."),
            ("Fitness & CrossFit", "fa-dumbbell", "Bodybuilding, functional fitness, and community fitness workshops."),
        ]

        sport_objs = {}
        for name, icon, desc in sports:
            obj, _ = SportsCategory.objects.get_or_create(
                name=name,
                defaults={'icon_class': icon, 'description': desc}
            )
            sport_objs[name] = obj
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(sport_objs)} Sports Categories."))

        # 2. Create Event Categories
        event_cats = [
            ("Championship / Cup", "fa-trophy"),
            ("Friendly Match / Showcase", "fa-handshake"),
            ("Marathon & Road Race", "fa-person-running"),
            ("Training Camp & Combine", "fa-campground"),
            ("Scouting Tournament", "fa-binoculars"),
        ]

        event_cat_objs = {}
        for name, icon in event_cats:
            obj, _ = EventCategory.objects.get_or_create(
                name=name,
                defaults={'icon_class': icon}
            )
            event_cat_objs[name] = obj
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(event_cat_objs)} Event Categories."))

        # 3. Create Superuser Admin
        admin_user, created = User.objects.get_or_create(
            username='sportiva_admin',
            defaults={
                'email': 'admin@sportiva.global',
                'first_name': 'Global',
                'last_name': 'Administrator',
                'role': User.Role.ORGANIZATION,
                'city': 'Geneva',
                'country': 'Switzerland',
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin2026!')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("[OK] Created superuser 'sportiva_admin' (pass: Admin2026!)"))

        # 4. Create Athletes
        athletes_data = [
            {
                'username': 'marcus_bolt',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'email': 'marcus@sportiva.global',
                'role': User.Role.ATHLETE,
                'sport': sport_objs['Athletics'],
                'favorite_sports': ['Athletics', 'Fitness & CrossFit'],
                'city': 'London',
                'country': 'United Kingdom',
                'bio': '100m & 200m Olympic hopeful. World Athletics Under-23 Gold Medalist. Dedicated to clean speed and elite discipline.',
                'sport_tier': 'ELITE',
                'exploits': [
                    {
                        'title': 'Gold Medal 100m Sprint (9.92s)',
                        'category': 'RECORD',
                        'competition': 'European U23 Athletics Championships',
                        'date': timezone.now().date() - timedelta(days=120),
                        'merit_points': 45,
                        'description': 'Broke national U23 record in final sprint heat with wind legal +1.2m/s.',
                    },
                    {
                        'title': 'National Senior Championship Victory',
                        'category': 'TITLE',
                        'competition': 'British National Athletics Trials',
                        'date': timezone.now().date() - timedelta(days=40),
                        'merit_points': 35,
                        'description': 'Qualified as first seed for the World Athletics Championship.',
                    }
                ]
            },
            {
                'username': 'elena_rodriguez',
                'first_name': 'Elena',
                'last_name': 'Rodriguez',
                'email': 'elena@sportiva.global',
                'role': User.Role.ATHLETE,
                'sport': sport_objs['Tennis'],
                'favorite_sports': ['Tennis', 'Fitness & CrossFit'],
                'city': 'Barcelona',
                'country': 'Spain',
                'bio': 'WTA ranked top 40 tennis professional. Fast baseline attacker, clay-court specialist, and sports science advocate.',
                'sport_tier': 'PRO',
                'exploits': [
                    {
                        'title': 'Catalonia Open Trophy Champion',
                        'category': 'TITLE',
                        'competition': 'WTA 250 International Open',
                        'date': timezone.now().date() - timedelta(days=85),
                        'merit_points': 40,
                        'description': 'Won all 5 rounds without dropping a set on clay.',
                    }
                ]
            },
            {
                'username': 'samuel_etame',
                'first_name': 'Samuel',
                'last_name': 'Etame',
                'email': 'samuel@sportiva.global',
                'role': User.Role.ATHLETE,
                'sport': sport_objs['Football'],
                'favorite_sports': ['Football', 'Basketball'],
                'city': 'Paris',
                'country': 'France',
                'bio': 'Dynamic forward and playmaker. Top scorer in Regional Youth League with 28 goals in 22 matches.',
                'sport_tier': 'CHAMPION',
                'exploits': [
                    {
                        'title': 'Top Goalscorer Golden Boot (28 Goals)',
                        'category': 'TITLE',
                        'competition': 'Ile-de-France Youth Cup',
                        'date': timezone.now().date() - timedelta(days=60),
                        'merit_points': 30,
                        'description': 'Scored hat-trick in the tournament grand final.',
                    }
                ]
            }
        ]

        athlete_users = {}
        for a_data in athletes_data:
            user, created = User.objects.get_or_create(
                username=a_data['username'],
                defaults={
                    'first_name': a_data['first_name'],
                    'last_name': a_data['last_name'],
                    'email': a_data['email'],
                    'role': a_data['role'],
                    'favorite_sports': a_data['favorite_sports'],
                    'city': a_data['city'],
                    'country': a_data['country'],
                    'bio': a_data['bio'],
                    'is_verified': True,
                    'instagram': a_data['username'],
                }
            )
            if created:
                user.set_password('Pass2026!')
                user.save()
            athlete_users[a_data['username']] = user

            # Seed exploits
            for exp in a_data['exploits']:
                AthleteExploit.objects.get_or_create(
                    athlete=user,
                    title=exp['title'],
                    defaults={
                        'category': exp['category'],
                        'competition_name': exp['competition'],
                        'date_achieved': exp['date'],
                        'score_points': exp['merit_points'],
                        'description': exp['description'],
                        'status': 'VERIFIED',
                        'validated_by': admin_user,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(athlete_users)} Athletes with Verified Exploits & Scores."))

        # 5. Create Global Sponsors & Profiles
        sponsors_data = [
            {
                'username': 'apex_nutrition',
                'company': 'Apex Performance Nutrition',
                'industry': 'Sports Nutrition & Hydration',
                'budget': '$50,000 - $150,000 / 30M - 90M FCFA',
                'city': 'Berlin',
                'country': 'Germany',
                'website': 'https://apexnutrition.example.com',
                'desc': 'Global sports nutrition brand supporting elite and aspiring endurance athletes worldwide.',
                'what_we_offer': 'Monthly nutrition stipends, hydration packs, sports science support, and tournament bonuses.',
                'requirements': 'Proven track record in national/international championships, Sportiva Score > 150.',
            },
            {
                'username': 'stride_footwear',
                'company': 'Stride Global Athletics Gear',
                'industry': 'Sportswear & Footwear',
                'budget': '$100,000 - $300,000 / 60M - 180M FCFA',
                'city': 'New York',
                'country': 'United States',
                'website': 'https://stridegear.example.com',
                'desc': 'Empowering track & field and tennis competitors with state-of-the-art performance wear.',
                'what_we_offer': 'Full seasonal footwear supply, racing spikes, global digital campaign visibility.',
                'requirements': 'Active competition calendar, podium contenders, high sportsmanship standards.',
            }
        ]

        sponsor_profiles = {}
        for s_data in sponsors_data:
            s_user, created = User.objects.get_or_create(
                username=s_data['username'],
                defaults={
                    'first_name': s_data['company'].split()[0],
                    'last_name': 'Official',
                    'email': f"contact@{s_data['username']}.com",
                    'role': User.Role.SPONSOR,
                    'city': s_data['city'],
                    'country': s_data['country'],
                    'is_verified': True,
                }
            )
            if created:
                s_user.set_password('Pass2026!')
                s_user.save()

            sp, _ = SponsorProfile.objects.get_or_create(
                user=s_user,
                defaults={
                    'company_name': s_data['company'],
                    'industry': s_data['industry'],
                    'annual_budget_range': s_data['budget'],
                    'city': s_data['city'],
                    'country': s_data['country'],
                    'website': s_data['website'],
                    'sports_supported': ['Athletics', 'Tennis', 'Football'],
                    'what_we_offer': s_data['what_we_offer'],
                    'requirements_criteria': s_data['requirements'],
                    'is_verified': True,
                }
            )
            sponsor_profiles[s_data['username']] = sp

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(sponsor_profiles)} Sponsors with Verified Profiles."))

        # 6. Create Formal Sponsorship Contracts & Requests
        marcus = athlete_users['marcus_bolt']
        stride_sponsor_user = sponsor_profiles['stride_footwear'].user

        SponsorshipContract.objects.get_or_create(
            contract_number="SPT-CTR-2026-0042",
            defaults={
                'title': "Global Sprint Championship Official Endorsement",
                'sponsor': stride_sponsor_user,
                'athlete': marcus,
                'financial_value': "$45,000 / 27,000,000 FCFA",
                'terms_and_conditions': 'Footwear testing, branding patch on official racing kit, 4 promotional social posts.',
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timedelta(days=365),
                'status': 'ACTIVE',
                'sponsor_signed': True,
                'beneficiary_signed': True,
            }
        )

        SponsorshipRequest.objects.get_or_create(
            sender=athlete_users['elena_rodriguez'],
            recipient_sponsor=sponsor_profiles['apex_nutrition'].user,
            defaults={
                'title': 'International Clay Court Season Fueling Partnership',
                'proposal_type': 'ATHLETE_TO_SPONSOR',
                'amount': '$20,000 / 12,000,000 FCFA',
                'deliverables_description': 'Seeking nutrition partnership for European tour. Projected visibility across 6 major WTA tournaments.',
                'perks_offered': 'Logo on tennis warm-up gear, 3 Instagram shoutouts per tournament, product testing feedback.',
                'status': 'ACCEPTED',
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Seeded Active Sponsorship Contract and Bidirectional Requests."))

        # 7. Create Global Sports Organizations / Clubs
        club_user, created = User.objects.get_or_create(
            username='olympic_academy',
            defaults={
                'first_name': 'London',
                'last_name': 'Athletics Club',
                'email': 'contact@londonathletics.org',
                'role': User.Role.ORGANIZATION,
                'city': 'London',
                'country': 'United Kingdom',
                'is_verified': True,
            }
        )
        if created:
            club_user.set_password('Pass2026!')
            club_user.save()

        org_profile, _ = OrganizationProfile.objects.get_or_create(
            user=club_user,
            defaults={
                'name': 'London Olympic Athletics High Performance Centre',
                'sports_category': sport_objs['Athletics'],
                'city': 'London',
                'country': 'United Kingdom',
                'address': 'Queen Elizabeth Olympic Park, London E20 2ST',
                'latitude': 51.5387,
                'longitude': -0.0166,
                'description': 'World-class track and field training center preparing international athletes for global championships.',
                'is_verified': True,
                'website': 'https://queenelizabetholympicpark.co.uk',
            }
        )

        # 8. Create Global Events with Capacity & Entry Fee
        event1, _ = Event.objects.get_or_create(
            title="SPORTIVA World Sprint & Relay Grand Prix",
            defaults={
                'organizer': club_user,
                'category': event_cat_objs['Championship / Cup'],
                'sport': sport_objs['Athletics'],
                'venue_name': 'London Stadium',
                'city': 'London',
                'country': 'United Kingdom',
                'latitude': 51.5387,
                'longitude': -0.0166,
                'start_date': timezone.now() + timedelta(days=25),
                'end_date': timezone.now() + timedelta(days=26),
                'description': 'Premier international track competition featuring top sprinters from over 40 nations.',
                'entry_fee': 45.0,
                'currency': 'USD',
                'max_participants': 250,
            }
        )

        event2, _ = Event.objects.get_or_create(
            title="Global Youth Football Invitational Cup",
            defaults={
                'organizer': admin_user,
                'category': event_cat_objs['Scouting Tournament'],
                'sport': sport_objs['Football'],
                'venue_name': 'Parc des Princes Sports Complex',
                'city': 'Paris',
                'country': 'France',
                'latitude': 48.8414,
                'longitude': 2.2530,
                'start_date': timezone.now() + timedelta(days=40),
                'end_date': timezone.now() + timedelta(days=42),
                'description': 'Elite scouting tournament for emerging young talents with international scouts in attendance.',
                'entry_fee': 0.0,
                'currency': 'USD',
                'max_participants': 500,
            }
        )

        # Seed Event Registration
        EventRegistration.objects.get_or_create(
            event=event1,
            user=marcus,
            defaults={
                'status': 'CONFIRMED',
                'payment_status': 'COMPLETED',
                'payment_method': 'CARD',
                'amount_paid': 45,
                'currency': 'USD',
                'registration_code': 'SPT-REG-2026-MARCUS',
                'invoice_number': 'INV-2026-0001',
                'organizer_validated': True,
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Seeded International Events & Registration Passes."))

        # 9. Create Fan / Visitor
        fan_user, created = User.objects.get_or_create(
            username='lucas_fan',
            defaults={
                'first_name': 'Lucas',
                'last_name': 'Moretti',
                'email': 'lucas@sportiva.global',
                'role': User.Role.VISITOR,
                'city': 'Rome',
                'country': 'Italy',
                'favorite_sports': ['Athletics', 'Football'],
                'bio': 'Passionate sports enthusiast following world records and rising football prospects.',
            }
        )
        if created:
            fan_user.set_password('Pass2026!')
            fan_user.save()

        # Follow relationships
        Follow.objects.get_or_create(follower=fan_user, followed_user=marcus)
        Follow.objects.get_or_create(follower=fan_user, followed_user=athlete_users['samuel_etame'])

        # 10. Seed Media Feed Posts & Shorts
        Post.objects.get_or_create(
            author=marcus,
            content="Official: Clocked 9.92s in the final heat today! Immense gratitude to my training team and sponsors. The road to glory continues! #SprintLife #WorldAthletics",
            defaults={
                'sport': sport_objs['Athletics'],
                'post_type': 'TEXT',
                'is_short': False,
                'views_count': 8950,
                'hashtags': '#SprintLife #WorldAthletics #GoldMedal',
            }
        )

        Post.objects.get_or_create(
            author=athlete_users['elena_rodriguez'],
            content="Intensive serve drill before next week's tournament. Focus, power, precision.",
            defaults={
                'sport': sport_objs['Tennis'],
                'post_type': 'SHORT',
                'is_short': True,
                'video_url': 'https://assets.mixkit.co/videos/preview/mixkit-tennis-player-bouncing-ball-with-racket-41123-large.mp4',
                'views_count': 5400,
                'hashtags': '#Tennis #Shorts #Training',
            }
        )

        # 11. Seed Direct Chat Conversation
        conv, _ = Conversation.objects.get_or_create(
            subject="Chat between Marcus and Stride Gear"
        )
        conv.participants.add(marcus, stride_sponsor_user)

        ChatMessage.objects.get_or_create(
            conversation=conv,
            sender=stride_sponsor_user,
            content="Marcus, extraordinary run this weekend! We are shipping the custom carbon spikes for your next race.",
            defaults={'is_read': True}
        )

        ChatMessage.objects.get_or_create(
            conversation=conv,
            sender=marcus,
            content="Thank you! The support makes all the difference. Ready to break the national record next week.",
            defaults={'is_read': True}
        )

        # 12. Seed Crowdfunding Campaign
        camp, _ = Campaign.objects.get_or_create(
            creator=marcus,
            title="Olympic Training Camp Preparation & Biomechanical Analysis",
            defaults={
                'category': 'TRAINING',
                'description': 'Raising funds for advanced 3D motion tracking analysis and altitude training camp in St. Moritz.',
                'target_amount': 8000,
                'raised_amount': 3200,
                'city': 'London',
                'country': 'United Kingdom',
                'latitude': 51.5074,
                'longitude': -0.1278,
                'deadline': timezone.now().date() + timedelta(days=60),
                'whatsapp_number': '+447911123456',
            }
        )

        Pledge.objects.get_or_create(
            campaign=camp,
            sponsor=fan_user,
            amount=200,
            defaults={
                'message': 'Good luck Marcus! Bring back the gold!',
                'is_anonymous': False,
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded Media Feed Stories, Shorts, Campaigns, and Direct Messages."))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] SPORTIVA global database seeded successfully!"))
