from django.db import models
from django.conf import settings


class SportsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, default='fa-trophy', help_text="FontAwesome icon class")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Sports Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class OrganizationProfile(models.Model):
    CITY_CHOICES = [
        ('Yaoundé', 'Yaoundé'),
        ('Douala', 'Douala'),
        ('Bafoussam', 'Bafoussam'),
        ('Garoua', 'Garoua'),
        ('Bamenda', 'Bamenda'),
        ('Buea', 'Buea'),
        ('Maroua', 'Maroua'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organization_profile'
    )
    name = models.CharField(max_length=200)
    sports_category = models.ForeignKey(
        SportsCategory,
        on_delete=models.CASCADE,
        related_name='organizations'
    )
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default='Yaoundé')
    address = models.CharField(max_length=255, help_text="Physical address or neighborhood")
    latitude = models.FloatField(default=3.8480, help_text="GPS Latitude for Leaflet Map")
    longitude = models.FloatField(default=11.5021, help_text="GPS Longitude for Leaflet Map")
    description = models.TextField(help_text="Overview of the club, academy, or facility")
    logo = models.ImageField(upload_to='organizations/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="WhatsApp contact format e.g. +237699000000")
    email = models.EmailField(blank=True)
    is_verified = models.BooleanField(default=False, help_text="Verified profile badge")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean_whatsapp(self):
        if not self.whatsapp_number:
            return ""
        digits = "".join([c for c in self.whatsapp_number if c.isdigit()])
        if not digits.startswith("237") and len(digits) == 9:
            digits = "237" + digits
        return digits

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city})"
