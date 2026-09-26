import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import models
from django.db import transaction
from accounts.decorators import tab_required
from .models import Event, EventCategory, EventRegistration
from organizations.models import SportsCategory
from .forms import EventForm
from .services.invoice_generator import generate_event_invoice_pdf


@tab_required('events')
def events_list(request):
    """List of sports events and tournaments with country/sport filters and capacity indicators."""
    search_query = request.GET.get('search', '').strip()
    country_filter = request.GET.get('country', '').strip()
    city_filter = request.GET.get('city', '').strip()
    sport_filter = request.GET.get('sport', '')
    cat_filter = request.GET.get('category', '')

    queryset = Event.objects.select_related('organizer', 'category', 'sport', 'organization').filter(is_published=True)

    if search_query:
        queryset = queryset.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(venue_name__icontains=search_query) |
            models.Q(city__icontains=search_query) |
            models.Q(country__icontains=search_query)
        )
    if country_filter:
        queryset = queryset.filter(country__icontains=country_filter)
    if city_filter:
        queryset = queryset.filter(city__icontains=city_filter)
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
        'search_query': search_query,
        'selected_country': country_filter,
        'selected_city': city_filter,
        'selected_sport': sport_filter,
        'selected_category': cat_filter,
    }
    return render(request, 'events/list.html', context)


def event_detail(request, pk):
    """Detailed view for a single event with registration status, capacity count, and payment trigger."""
    event = get_object_or_404(
        Event.objects.select_related('organizer', 'category', 'sport', 'organization'),
        pk=pk
    )
    user_registration = None
    if request.user.is_authenticated:
        user_registration = EventRegistration.objects.filter(event=event, user=request.user).first()

    registrations = event.registrations.select_related('user').filter(payment_status__in=['COMPLETED', 'FREE'])[:12]
    is_organizer = request.user.is_authenticated and (request.user == event.organizer or request.user.is_staff)

    context = {
        'event': event,
        'user_registration': user_registration,
        'is_registered': user_registration is not None and user_registration.status != 'CANCELLED',
        'registrations': registrations,
        'confirmed_count': event.confirmed_participants_count(),
        'spots_remaining': event.spots_remaining(),
        'is_sold_out': event.is_sold_out(),
        'is_organizer': is_organizer,
    }
    return render(request, 'events/detail.html', context)


@login_required
def event_register_payment(request, pk):
    """
    Handles event registration and digital payment simulation.
    Verifies capacity limit (first to pay secures spot), creates invoice,
    generates PDF invoice and attaches it to registration.
    """
    event = get_object_or_404(Event, pk=pk)

    # Check if already registered (a CANCELLED registration may re-register)
    existing_reg = EventRegistration.objects.filter(event=event, user=request.user).first()
    if existing_reg and existing_reg.status != 'CANCELLED':
        messages.info(request, "You are already registered for this event. You can download your invoice below.")
        return redirect('event_detail', pk=pk)

    # Check capacity
    if event.is_sold_out():
        messages.error(request, "Sorry, this event has reached maximum capacity and is completely sold out.")
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'Credit Card (Visa/Mastercard)')
        team_name = request.POST.get('team_or_club_name', '').strip()

        # Payment details
        fee = event.fee_amount
        currency = event.currency
        invoice_num = f"INV-{timezone.now().year}-{uuid.uuid4().hex[:6].upper()}"

        # Lock the event row while re-checking capacity so two simultaneous
        # signups cannot take the last spot twice.
        with transaction.atomic():
            locked_event = Event.objects.select_for_update().get(pk=event.pk)
            if locked_event.is_sold_out():
                messages.error(request, "Sorry, this event has just sold out.")
                return redirect('event_detail', pk=pk)

            if existing_reg:
                # Re-register in place over the cancelled record
                reg = existing_reg
                reg.team_or_club_name = team_name
                reg.status = 'CONFIRMED'
                reg.payment_status = 'COMPLETED' if fee > 0 else 'FREE'
                reg.payment_method = payment_method
                reg.amount_paid = fee
                reg.currency = currency
                reg.invoice_number = invoice_num
                reg.organizer_validated = True
                reg.organizer_validation_notes = ''
            else:
                reg = EventRegistration(
                    event=event,
                    user=request.user,
                    team_or_club_name=team_name,
                    status='CONFIRMED',
                    payment_status='COMPLETED' if fee > 0 else 'FREE',
                    payment_method=payment_method,
                    amount_paid=fee,
                    currency=currency,
                    invoice_number=invoice_num,
                    organizer_validated=True,
                )
            reg.save()

        # Generate PDF Invoice and save to model
        try:
            pdf_bytes = generate_event_invoice_pdf(reg)
            reg.invoice_pdf.save(f"{invoice_num}.pdf", ContentFile(pdf_bytes), save=True)
        except Exception as e:
            print(f"Error generating PDF invoice: {e}")

        messages.success(
            request,
            f"Registration & payment completed successfully! 🎟️ Spot confirmed ({event.spots_remaining()} spots left). Your official PDF invoice #{invoice_num} is ready for download."
        )
        return redirect('event_detail', pk=pk)

    return redirect('event_detail', pk=pk)


@login_required
def download_invoice_pdf(request, pk):
    """Generates or downloads official SPORTIVA PDF invoice for a registration."""
    registration = get_object_or_404(EventRegistration, pk=pk)
    
    # Permission check: must be owner or organizer or staff
    if request.user != registration.user and request.user != registration.event.organizer and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this invoice.")
        return redirect('home')

    # Generate fresh PDF on the fly or serve existing
    pdf_bytes = generate_event_invoice_pdf(registration)
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{registration.invoice_number}_SPORTIVA_Invoice.pdf"'
    return response


@login_required
def validate_registration_view(request, pk):
    """Allows event organizers to validate / check-in participants."""
    registration = get_object_or_404(EventRegistration, pk=pk)
    if request.user != registration.event.organizer and not request.user.is_staff:
        messages.error(request, "Only the event organizer can validate participants.")
        return redirect('event_detail', pk=registration.event.pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('validation_notes', '').strip()
        if action == 'VALIDATE':
            registration.organizer_validated = True
            registration.organizer_validation_notes = notes
            registration.status = 'CONFIRMED'
            registration.save()
            messages.success(request, f"Participant {registration.user.username} has been verified and rostered!")
        elif action == 'CANCEL':
            registration.status = 'CANCELLED'
            registration.save()
            messages.warning(request, f"Registration for {registration.user.username} has been cancelled.")

    return redirect('event_detail', pk=registration.event.pk)


@login_required
def cancel_registration(request, pk):
    """
    Allows a registered user to cancel (withdraw) their own event registration.
    Frees up the spot immediately and marks the registration as CANCELLED.
    """
    registration = get_object_or_404(EventRegistration, pk=pk)

    # Only the registrant themselves (or staff) may cancel
    if request.user != registration.user and not request.user.is_staff:
        messages.error(request, "You can only cancel your own registration.")
        return redirect('event_detail', pk=registration.event.pk)

    if registration.status == 'CANCELLED':
        messages.info(request, "This registration is already cancelled.")
        return redirect('event_detail', pk=registration.event.pk)

    if request.method == 'POST':
        event_pk = registration.event.pk
        registration.status = 'CANCELLED'
        registration.payment_status = 'REFUNDED'
        registration.organizer_validation_notes = (
            f"Cancelled by {request.user.username} on "
            f"{timezone.now().strftime('%d %b %Y %H:%M')}"
        )
        registration.save()
        messages.warning(
            request,
            f"Your registration for '{registration.event.title}' has been cancelled. "
            "The spot has been released. If you paid, a refund record has been created."
        )
        return redirect('event_detail', pk=event_pk)

    # GET → show confirmation page
    return render(request, 'events/cancel_registration_confirm.html', {
        'registration': registration,
        'event': registration.event,
    })


@login_required
def delete_event(request, pk):
    """
    Allows the event organiser (or staff) to delete/unpublish an event.
    Presents a confirmation screen first; POST actually deletes.
    """
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.organizer and not request.user.is_staff:
        messages.error(request, "Only the event organiser can delete this event.")
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f"Event '{title}' has been permanently deleted.")
        return redirect('events_list')

    return render(request, 'events/delete_event_confirm.html', {'event': event})


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
