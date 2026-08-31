import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings

def home(request):
    """
    Landing Page for Sportiva CM.
    Renders top stats, featured events, organizations, media, marketplace, and sponsorships.
    """
    context = {
        'stats': {
            'athletes': 1250,
            'clubs': 84,
            'events': 32,
            'sponsorships_raised': '15,000,000 FCFA',
        }
    }
    return render(request, 'core/home.html', context)

def offline_view(request):
    """
    Offline fallback page when network is disconnected.
    """
    return render(request, 'offline.html')

def service_worker(request):
    """
    Serve sw.js from static directory with root scope.
    """
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if os.path.exists(sw_path):
        with open(sw_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/javascript')
    return HttpResponse("// sw not found", content_type='application/javascript')

def manifest(request):
    """
    Serve manifest.json.
    """
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/json')
    return HttpResponse("{}", content_type='application/json')
