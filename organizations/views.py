from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from accounts.decorators import tab_required
from .models import OrganizationProfile, SportsCategory
from .forms import OrganizationProfileForm


@tab_required('organizations')
def organizations_list(request):
    """
    Renders list of sports clubs, academies, and organizations with search and filtering.
    """
    search_query = request.GET.get('search', '').strip()
    country_filter = request.GET.get('country', '').strip()
    city_filter = request.GET.get('city', '').strip()
    sport_filter = request.GET.get('sport', '')

    queryset = OrganizationProfile.objects.select_related('sports_category').all()

    if search_query:
        queryset = queryset.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(city__icontains=search_query) |
            models.Q(country__icontains=search_query)
        )
    if country_filter:
        queryset = queryset.filter(country__icontains=country_filter)
    if city_filter:
        queryset = queryset.filter(city__icontains=city_filter)
    if sport_filter:
        queryset = queryset.filter(sports_category__id=sport_filter)

    categories = SportsCategory.objects.all()

    context = {
        'organizations': queryset,
        'categories': categories,
        'search_query': search_query,
        'selected_country': country_filter,
        'selected_city': city_filter,
        'selected_sport': sport_filter,
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
        form = OrganizationProfileForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save(commit=False)
            org.user = request.user
            org.save()
            messages.success(request, f"Organization '{org.name}' created successfully!")
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationProfileForm()
    return render(request, 'organizations/create.html', {'form': form})
