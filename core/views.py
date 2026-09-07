import os
import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
from accounts.models import User
from events.models import Event
from media_feed.models import Post, Like
from media_feed.views import PostForm
from sponsorships.models import SponsorProfile, Campaign
from organizations.models import SportsCategory


# ─── CURATED GLOBAL SPORTS NEWS (OFFLINE-READY BUILT-IN DATA) ────────────────
# These articles are always available. When online, a real API can override.
BUILT_IN_NEWS = [
    {
        "title": "Erling Haaland breaks another Champions League scoring record in dramatic comeback",
        "discipline": "Football",
        "icon": "⚽",
        "source": "UEFA Sport",
        "url": "#",
        "published_at": "2026-09-04T10:00:00Z",
    },
    {
        "title": "Sha'Carri Richardson dominates 100m final at World Athletics Championships with new personal best",
        "discipline": "Athletics",
        "icon": "🏃",
        "source": "World Athletics",
        "url": "#",
        "published_at": "2026-09-04T09:30:00Z",
    },
    {
        "title": "Paris Olympics 2028: Record 200 nations to participate as global sports grows",
        "discipline": "Athletics",
        "icon": "🏅",
        "source": "IOC Press",
        "url": "#",
        "published_at": "2026-09-04T09:00:00Z",
    },
    {
        "title": "LeBron James announces new global youth basketball development foundation",
        "discipline": "Basketball",
        "icon": "🏀",
        "source": "NBA Global",
        "url": "#",
        "published_at": "2026-09-04T08:45:00Z",
    },
    {
        "title": "Novak Djokovic advances to US Open quarterfinals in five-set thriller",
        "discipline": "Tennis",
        "icon": "🎾",
        "source": "ATP Tour",
        "url": "#",
        "published_at": "2026-09-04T08:00:00Z",
    },
    {
        "title": "South Africa defeat All Blacks in historic Rugby Championship clash",
        "discipline": "Rugby",
        "icon": "🏉",
        "source": "World Rugby",
        "url": "#",
        "published_at": "2026-09-03T21:00:00Z",
    },
    {
        "title": "Léon Marchand sets new world record in 400m IM at Grand Prix Budapest",
        "discipline": "Swimming",
        "icon": "🏊",
        "source": "World Aquatics",
        "url": "#",
        "published_at": "2026-09-03T18:30:00Z",
    },
    {
        "title": "Tadej Pogačar and Jonas Vingegaard confirm Vuelta a España rivalry in mountain stage",
        "discipline": "Cycling",
        "icon": "🚴",
        "source": "Cycling News",
        "url": "#",
        "published_at": "2026-09-03T17:00:00Z",
    },
    {
        "title": "India win T20 World Cup cricket title in thrilling final against England",
        "discipline": "Cricket",
        "icon": "🏏",
        "source": "ICC Sport",
        "url": "#",
        "published_at": "2026-09-03T15:00:00Z",
    },
    {
        "title": "Iga Świątek wins third Grand Slam of the season to clinch world number one ranking",
        "discipline": "Tennis",
        "icon": "🎾",
        "source": "WTA Tour",
        "url": "#",
        "published_at": "2026-09-03T12:00:00Z",
    },
    {
        "title": "Africa Cup of Nations: Morocco and Senegal set for blockbuster semi-final clash",
        "discipline": "Football",
        "icon": "⚽",
        "source": "CAF Sport",
        "url": "#",
        "published_at": "2026-09-03T11:00:00Z",
    },
    {
        "title": "MMA: Conor McGregor announces comeback fight against rising Brazilian champion",
        "discipline": "Combat",
        "icon": "🥊",
        "source": "UFC News",
        "url": "#",
        "published_at": "2026-09-03T09:00:00Z",
    },
]


def home(request):
    """
    Instagram-Style Homepage for SPORTIVA:
    Features top stories/shorts carousel, personalized 'For You' dynamic feed based
    on user's registered sports preferences, top athletes leaderboard, upcoming events,
    and verified sponsors.
    """
    # 1. Shorts / Stories Carousel
    top_shorts = Post.objects.filter(is_published=True, is_short=True).select_related('author', 'sport')[:12]

    # 2. Dynamic Feed Posts (Personalized by favorite sports if user is logged in)
    all_posts = list(Post.objects.filter(is_published=True).select_related('author', 'sport').prefetch_related('likes', 'comments')[:25])

    if request.user.is_authenticated and request.user.favorite_sports:
        user_sports = [s.lower() for s in request.user.favorite_sports]
        def sort_by_preference(post):
            if post.sport and post.sport.name.lower() in user_sports:
                return 0
            return 1
        all_posts.sort(key=sort_by_preference)

    liked_post_ids = set()
    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

    # 3. Top Athletes Leaderboard
    top_athletes = [u for u in User.objects.filter(role=User.Role.ATHLETE, is_active=True)]
    top_athletes.sort(key=lambda u: u.sportiva_score, reverse=True)
    top_athletes = top_athletes[:5]

    # 4. Featured Events
    featured_events = Event.objects.filter(is_published=True).select_related('organizer', 'sport')[:4]

    # 5. Featured Sponsors
    featured_sponsors = SponsorProfile.objects.all().select_related('user')[:4]

    sports_categories = SportsCategory.objects.all()

    context = {
        'top_shorts': top_shorts,
        'posts': all_posts,
        'liked_post_ids': liked_post_ids,
        'post_form': PostForm(),
        'top_athletes': top_athletes,
        'featured_events': featured_events,
        'featured_sponsors': featured_sponsors,
        'sports_categories': sports_categories,
        'latest_news': BUILT_IN_NEWS[:6],  # Pre-render top 6 articles server-side
        'stats': {
            'athletes': User.objects.filter(role=User.Role.ATHLETE).count() or 1450,
            'clubs': User.objects.filter(role=User.Role.ORGANIZATION).count() or 95,
            'events': Event.objects.count() or 42,
            'sponsors': SponsorProfile.objects.count() or 18,
        }
    }
    return render(request, 'core/home.html', context)


def offline_view(request):
    """Offline fallback page when network is disconnected."""
    return render(request, 'offline.html')


def service_worker(request):
    """Serve sw.js from static directory with root scope."""
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if os.path.exists(sw_path):
        with open(sw_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/javascript')
    return HttpResponse("// sw not found", content_type='application/javascript')


def manifest(request):
    """Serve manifest.json."""
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/json')
    return HttpResponse("{}", content_type='application/json')


def sports_news_api(request):
    """
    JSON API for live sports news ticker.
    Returns curated built-in news articles (works offline).
    Can be extended to integrate a real-time sports API (e.g., NewsAPI, SportMonks).
    The Service Worker will cache this response for offline use.
    """
    # Always return built-in curated news (reliable offline + online)
    # To integrate a real API: fetch from external endpoint here and merge/override
    return JsonResponse({
        'status': 'ok',
        'online': True,
        'count': len(BUILT_IN_NEWS),
        'articles': BUILT_IN_NEWS,
        'last_updated': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    }, json_dumps_params={'ensure_ascii': False})

