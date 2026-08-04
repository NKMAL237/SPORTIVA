from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventCategory, EventAttendance
from organizations.models import SportsCategory
from .forms import EventForm


def events_list(request):
    """List of sports events and tournaments with filter options."""
    city_filter = request.GET.get('city', '')
    sport_filter = request.GET.get('sport', '')
    cat_filter = request.GET.get('category', '')

    queryset = Event.objects.select_related('organizer', 'category', 'sport', 'organization').filter(is_published=True)

    if city_filter:
        queryset = queryset.filter(city=city_filter)
    if sport_filter:
        queryset = queryset.filter(sport__id=sport_filter)
    if cat_filter:
        queryset = queryset.filter(category__id=cat_filter)

    categories = EventCategory.objects.all()
    sports = SportsCategory.objects.all()

    context = {
        'events': queryset,
        'categories': categories,
        'sports': sports,
        'selected_city': city_filter,
        'selected_sport': sport_filter,
        'selected_category': cat_filter,
    }
    return render(request, 'events/list.html', context)


def event_detail(request, pk):
    """Detailed view for a single event."""
    event = get_object_or_404(
        Event.objects.select_related('organizer', 'category', 'sport', 'organization'),
        pk=pk
    )
    is_attending = False
    if request.user.is_authenticated:
        is_attending = EventAttendance.objects.filter(event=event, user=request.user).exists()

    attendances = EventAttendance.objects.filter(event=event).select_related('user')[:10]

    context = {
        'event': event,
        'is_attending': is_attending,
        'attendances': attendances,
        'attendee_count': event.attendances.count(),
    }
    return render(request, 'events/detail.html', context)


@login_required
def event_create(request):
    """Create a new sports tournament or event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/create.html', {'form': form})


@login_required
def event_rsvp(request, pk):
    """Toggle user RSVP attendance for an event."""
    event = get_object_or_404(Event, pk=pk)
    attendance, created = EventAttendance.objects.get_or_create(event=event, user=request.user)

    if not created:
        attendance.delete()
        messages.info(request, f"You have unregistered from '{event.title}'.")
    else:
        messages.success(request, f"You are now registered for '{event.title}'!")

    return redirect('event_detail', pk=event.pk)
