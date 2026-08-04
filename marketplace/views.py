from django.shortcuts import render

def marketplace_list(request):
    """Marketplace for buying and selling sports gear."""
    return render(request, 'marketplace/list.html')
