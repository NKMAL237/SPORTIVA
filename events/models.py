from django.db import models
from django.conf import settings
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
    CITY_CHOICES = OrganizationProfile.CITY_CHOICES

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
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default='Yaoundé')
    venue_name = models.CharField(max_length=200, help_text="e.g. Stade Ahmadou Ahidjo")
    latitude = models.FloatField(default=3.8864, help_text="GPS Latitude")
    longitude = models.FloatField(default=11.5367, help_text="GPS Longitude")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    banner = models.ImageField(upload_to='events/', blank=True, null=True)
    contact_whatsapp = models.CharField(max_length=20, blank=True)
    entry_fee = models.CharField(max_length=100, default='Free', help_text="e.g. Free or 1,000 FCFA")
    max_participants = models.PositiveIntegerField(default=100)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean_whatsapp(self):
        if not self.contact_whatsapp:
            return ""
        digits = "".join([c for c in self.contact_whatsapp if c.isdigit()])
        if not digits.startswith("237") and len(digits) == 9:
            digits = "237" + digits
        return digits

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} - {self.city} ({self.start_date.strftime('%d %b %Y')})"


class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_attendances')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} attending {self.event.title}"
