from django.shortcuts import render

def media_feed_list(request):
    """News feed, sports videos, and articles."""
    return render(request, 'media_feed/list.html')
