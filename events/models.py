import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from organizations.models import SportsCategory, OrganizationProfile


class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, default='fa-calendar-days')

    class Meta:
        verbose_name_plural = "Event Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    organization = models.ForeignKey(
        OrganizationProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.CASCADE,
        related_name='events'
    )
    sport = models.ForeignKey(
        SportsCategory,
        on_delete=models.CASCADE,
        related_name='events'
    )
    country = models.CharField(max_length=100, default='Global')
    city = models.CharField(max_length=100, default='Global City')
    venue_name = models.CharField(max_length=200, help_text="e.g. Olympic Stadium, Madison Square Garden")
    latitude = models.FloatField(default=3.8864, help_text="GPS Latitude")
    longitude = models.FloatField(default=11.5367, help_text="GPS Longitude")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    banner = models.ImageField(upload_to='events/', blank=True, null=True)
    contact_whatsapp = models.CharField(max_length=30, blank=True)
    entry_fee = models.CharField(max_length=100, default='Free', help_text="e.g. Free, $25, or 5,000 FCFA")
    fee_amount = models.PositiveIntegerField(default=0, help_text="Numeric entry fee for checkout (0 for free)")
    currency = models.CharField(max_length=10, default='USD', help_text="USD, EUR, FCFA, GBP")
    max_participants = models.PositiveIntegerField(default=50, help_text="Maximum capacity of participants")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean_whatsapp(self):
        if not self.contact_whatsapp:
            return ""
        return "".join([c for c in self.contact_whatsapp if c.isdigit()])

    def confirmed_participants_count(self):
        return self.registrations.filter(payment_status__in=['COMPLETED', 'FREE']).count()

    def spots_remaining(self):
        return max(0, self.max_participants - self.confirmed_participants_count())

    def is_sold_out(self):
        return self.spots_remaining() <= 0

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} - {self.city}, {self.country} ({self.start_date.strftime('%d %b %Y')})"


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed & Active'),
        ('PENDING_VALIDATION', 'Pending Organizer Validation'),
        ('CANCELLED', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('COMPLETED', 'Payment Completed'),
        ('FREE', 'Free Registration'),
        ('PENDING', 'Payment Pending'),
        ('REFUNDED', 'Refunded'),
    ]

    registration_code = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    team_or_club_name = models.CharField(max_length=150, blank=True, help_text="Athlete Team / Club / Independent")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='CONFIRMED')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='COMPLETED')
    payment_method = models.CharField(max_length=50, default='CARD', help_text="Credit Card, PayPal, MTN MoMo, Orange Money, Apple Pay, Google Pay, Crypto")
    amount_paid = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=10, default='USD')
    invoice_number = models.CharField(max_length=60, unique=True)
    invoice_pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    organizer_validated = models.BooleanField(default=True, help_text="Organizer confirmation of registration")
    organizer_validation_notes = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} -> {self.event.title} [Invoice: {self.invoice_number}]"


# Alias EventAttendance for backward-compatibility with existing code
EventAttendance = EventRegistration
