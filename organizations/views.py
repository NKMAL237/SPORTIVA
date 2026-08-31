import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import tab_required
from .models import OrganizationProfile, SportsCategory
from .forms import OrganizationForm


@tab_required('organizations')
def organizations_list(request):

    """
    Renders list of sports organizations with filtering by city and sport.
    Passes a JSON payload of organization coordinates for the Leaflet map.
    """
    city_filter = request.GET.get('city', '')
    sport_filter = request.GET.get('sport', '')

    queryset = OrganizationProfile.objects.select_related('sports_category').all()

    if city_filter:
        queryset = queryset.filter(city=city_filter)
    if sport_filter:
        queryset = queryset.filter(sports_category__id=sport_filter)

    categories = SportsCategory.objects.all()

    # Map locations data
    map_data = [
        {
            'id': org.id,
            'name': org.name,
            'city': org.city,
            'lat': org.latitude,
            'lng': org.longitude,
            'category': org.sports_category.name,
            'is_verified': org.is_verified,
        }
        for org in queryset
    ]

    context = {
        'organizations': queryset,
        'categories': categories,
        'selected_city': city_filter,
        'selected_sport': sport_filter,
        'map_data_json': json.dumps(map_data),
    }
    return render(request, 'organizations/list.html', context)


def organization_detail(request, pk):
    """Renders detailed view for a single sports organization."""
    org = get_object_or_404(OrganizationProfile.objects.select_related('sports_category'), pk=pk)
    events = org.events.filter(is_published=True)
    return render(request, 'organizations/detail.html', {'organization': org, 'events': events})


@login_required
def organization_create(request):
    """Create a new sports organization profile."""
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save(commit=False)
            org.user = request.user
            org.save()
            messages.success(request, f"Organization '{org.name}' created successfully!")
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/create.html', {'form': form})
