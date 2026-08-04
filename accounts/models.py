from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ATHLETE = 'ATHLETE', 'Athlete / Sports Enthusiast'
        ORGANIZATION = 'ORGANIZATION', 'Club / Academy / Organization'
        TRAINER = 'TRAINER', 'Coach / Personal Trainer'
        SPONSOR = 'SPONSOR', 'Sponsor / Business Partner'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ATHLETE,
        help_text="Primary role on Sportiva CM"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number for direct WhatsApp contact (e.g., +237699000000)"
    )
    city = models.CharField(
        max_length=100,
        default='Yaoundé',
        help_text="City in Cameroon (e.g., Yaoundé, Douala, Bafoussam, Garoua)"
    )
    bio = models.TextField(
        blank=True,
        help_text="Short bio or description"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile image"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Verified account badge"
    )

    def clean_phone_for_whatsapp(self):
        """Format phone number for WhatsApp web links."""
        if not self.phone_number:
            return ""
        digits = "".join([c for c in self.phone_number if c.isdigit()])
        if not digits.startswith("237") and len(digits) == 9:
            digits = "237" + digits
        return digits

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
