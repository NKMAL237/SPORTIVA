from django.db import models
from django.conf import settings


class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('TRAVEL', 'Tournament Travel & Transport'),
        ('EQUIPMENT', 'Sports Equipment & Gear'),
        ('TRAINING', 'Training & Coaching Fees'),
        ('VENUE', 'Venue Rental & Logistics'),
        ('MEDICAL', 'Medical & Sports Insurance'),
        ('OTHER', 'Other'),
    ]
    CITY_CHOICES = [
        ('Yaoundé', 'Yaoundé'),
        ('Douala', 'Douala'),
        ('Bafoussam', 'Bafoussam'),
        ('Garoua', 'Garoua'),
        ('Bamenda', 'Bamenda'),
        ('Buea', 'Buea'),
        ('Maroua', 'Maroua'),
    ]

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    description = models.TextField()
    target_amount = models.PositiveIntegerField(help_text="Target amount in FCFA")
    raised_amount = models.PositiveIntegerField(default=0, help_text="Amount raised so far in FCFA")
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default='Yaoundé')
    deadline = models.DateField(blank=True, null=True)
    banner = models.ImageField(upload_to='sponsorships/', blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return min(int((self.raised_amount / self.target_amount) * 100), 100)

    def clean_whatsapp(self):
        if not self.whatsapp_number:
            return ""
        digits = "".join([c for c in self.whatsapp_number if c.isdigit()])
        if not digits.startswith("237") and len(digits) == 9:
            digits = "237" + digits
        return digits

    def __str__(self):
        return f"{self.title} ({self.progress_percent()}% funded)"


class Pledge(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='pledges')
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    amount = models.PositiveIntegerField(help_text="Pledge amount in FCFA")
    message = models.TextField(blank=True, help_text="Optional sponsor message")
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        name = "Anonymous" if self.is_anonymous else self.sponsor.username
        return f"{name} pledged {self.amount:,} FCFA to {self.campaign.title}"
