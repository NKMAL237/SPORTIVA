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
    custom_allowed_tabs = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom tab access overrides e.g. {'events': True, 'sponsorships': False}"
    )

    ALL_TABS = [
        ('home', 'Home'),
        ('events', 'Events'),
        ('organizations', 'Organizations'),
        ('media_feed', 'News & Feed'),
        ('marketplace', 'Marketplace'),
        ('sponsorships', 'Sponsorships'),
        ('user_management', 'User Management'),
    ]

    DEFAULT_ROLE_TABS = {
        Role.ATHLETE: ['home', 'events', 'media_feed', 'marketplace'],
        Role.ORGANIZATION: ['home', 'events', 'organizations', 'media_feed', 'sponsorships'],
        Role.TRAINER: ['home', 'events', 'organizations', 'media_feed', 'marketplace'],
        Role.SPONSOR: ['home', 'organizations', 'media_feed', 'sponsorships'],
    }

    def get_allowed_tabs(self):
        """
        Returns list of tab keys that this user is allowed to access.
        Superusers and Staff get all tabs.
        Otherwise checks custom_allowed_tabs overrides, falling back to role defaults.
        """
        all_tab_keys = [t[0] for t in self.ALL_TABS]
        if self.is_superuser or self.is_staff:
            return all_tab_keys

        default_tabs = set(self.DEFAULT_ROLE_TABS.get(self.role, ['home', 'events', 'media_feed']))
        
        # Apply custom overrides if specified
        if isinstance(self.custom_allowed_tabs, dict) and self.custom_allowed_tabs:
            allowed = set()
            for tab_key in all_tab_keys:
                if tab_key in self.custom_allowed_tabs:
                    if self.custom_allowed_tabs[tab_key]:
                        allowed.add(tab_key)
                elif tab_key in default_tabs:
                    allowed.add(tab_key)
            return [t for t in all_tab_keys if t in allowed]

        return [t for t in all_tab_keys if t in default_tabs]

    def has_tab_access(self, tab_name):
        """Check if user has access to a specific tab."""
        return tab_name in self.get_allowed_tabs()

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

