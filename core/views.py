from django.shortcuts import render

def home(request):
    """
    Landing Page for Sportiva CM.
    Renders top stats, featured events, organizations, media, marketplace, and sponsorships.
    """
    # Dummy placeholder stats for initial landing page render
    context = {
        'stats': {
            'athletes': 1250,
            'clubs': 84,
            'events': 32,
            'sponsorships_raised': '15,000,000 FCFA',
        }
    }
    return render(request, 'core/home.html', context)
