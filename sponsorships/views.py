from django.shortcuts import render

def sponsorships_list(request):
    """Sponsorship campaigns for athletes and sports clubs."""
    return render(request, 'sponsorships/list.html')
