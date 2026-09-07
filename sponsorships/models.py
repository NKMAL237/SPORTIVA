from django.db import models
from django.conf import settings
from django.utils import timezone


class SponsorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sponsor_profile'
    )
    company_name = models.CharField(max_length=200)
    brand_tagline = models.CharField(max_length=255, blank=True, help_text="e.g. Empowering Next-Gen Global Champions")
    industry = models.CharField(max_length=100, default='Sports Apparel & Nutrition')
    annual_budget_range = models.CharField(
        max_length=100,
        default='$10,000 - $50,000 / 5M - 25M FCFA',
        help_text="Available sponsorship allocation"
    )
    sports_supported = models.JSONField(
        default=list,
        blank=True,
        help_text="Sports this sponsor invests in (e.g. ['Football', 'Athletics'])"
    )
    what_we_offer = models.TextField(
        help_text="What benefits the sponsor provides (e.g., Equipment, Financial Stipends, Travel Grants, Gear, Media Exposure)"
    )
    requirements_criteria = models.TextField(
        blank=True,
        help_text="What the sponsor looks for in athletes/events (e.g. Sportiva Score > 150, regional tournaments, social engagement)"
    )
    website = models.URLField(blank=True)
    country = models.CharField(max_length=100, default='Global')
    city = models.CharField(max_length=100, default='Global City')
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(default=3.8864, help_text="GPS Latitude for location popup")
    longitude = models.FloatField(default=11.5367, help_text="GPS Longitude for location popup")
    logo = models.ImageField(upload_to='sponsors/logos/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=True, help_text="Verified sponsor badge")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean_whatsapp(self):
        if not self.whatsapp_number:
            return ""
        return "".join([c for c in self.whatsapp_number if c.isdigit()])

    def __str__(self):
        return f"{self.company_name} ({self.country})"


class SponsorshipRequest(models.Model):
    TYPE_CHOICES = [
        ('ATHLETE_TO_SPONSOR', 'Athlete / Club Requesting Sponsorship'),
        ('SPONSOR_TO_ATHLETE', 'Sponsor Offering Partnership / Deal'),
        ('EVENT_SPONSORSHIP', 'Event Sponsorship Proposal'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Under Review / Pending'),
        ('ACCEPTED', 'Accepted / Agreed'),
        ('DECLINED', 'Declined'),
        ('CONVERTED_TO_CONTRACT', 'Converted to Contract'),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_proposals'
    )
    recipient_sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_sponsor_requests',
        null=True,
        blank=True
    )
    recipient_athlete = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_athlete_offers',
        null=True,
        blank=True
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sponsorship_proposals'
    )
    title = models.CharField(max_length=200, help_text="Proposal title e.g. Season 2026 Apparel & Travel Support")
    proposal_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='ATHLETE_TO_SPONSOR')
    amount = models.CharField(max_length=100, help_text="Proposed financial value or gear valuation (e.g. $5,000 / 2,500,000 FCFA)")
    deliverables_description = models.TextField(help_text="Detailed proposal, deliverables, branding placement, social exposure")
    perks_offered = models.TextField(blank=True, help_text="Logo on jersey, event banner placement, VIP passes, social shoutouts")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    response_message = models.TextField(blank=True, help_text="Feedback or counter-offer from recipient")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_proposal_type_display()}: {self.title} ({self.status})"


class SponsorshipContract(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft Proposal'),
        ('ACTIVE', 'Active & Enforced'),
        ('COMPLETED', 'Completed'),
        ('TERMINATED', 'Terminated'),
    ]

    contract_number = models.CharField(max_length=50, unique=True, help_text="e.g. SPT-CTR-2026-0042")
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sponsor_contracts'
    )
    athlete = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='athlete_contracts',
        null=True,
        blank=True
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='event_contracts'
    )
    title = models.CharField(max_length=200)
    financial_value = models.CharField(max_length=100, help_text="Contract value e.g. $15,000 / 7,500,000 FCFA")
    terms_and_conditions = models.TextField(help_text="Detailed contractual obligations, branding rules, performance bonuses")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    sponsor_signed = models.BooleanField(default=True)
    beneficiary_signed = models.BooleanField(default=True)
    signed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-signed_at']

    def __str__(self):
        target = self.athlete.username if self.athlete else (self.event.title if self.event else "Entity")
        return f"Contract #{self.contract_number}: {self.sponsor.username} <-> {target}"


class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('TRAVEL', 'Tournament Travel & Transport'),
        ('EQUIPMENT', 'Sports Equipment & Gear'),
        ('TRAINING', 'Training & Coaching Fees'),
        ('VENUE', 'Venue Rental & Logistics'),
        ('MEDICAL', 'Medical & Sports Insurance'),
        ('OTHER', 'Other'),
    ]

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    description = models.TextField()
    target_amount = models.PositiveIntegerField(help_text="Target amount (e.g. in FCFA or USD equivalent)")
    raised_amount = models.PositiveIntegerField(default=0, help_text="Amount raised so far")
    country = models.CharField(max_length=100, default='Global')
    city = models.CharField(max_length=100, default='Global City')
    latitude = models.FloatField(default=3.8864)
    longitude = models.FloatField(default=11.5367)
    deadline = models.DateField(blank=True, null=True)
    banner = models.ImageField(upload_to='sponsorships/', blank=True, null=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
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
        return "".join([c for c in self.whatsapp_number if c.isdigit()])

    def __str__(self):
        return f"{self.title} ({self.progress_percent()}% funded)"


class Pledge(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='pledges')
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    amount = models.PositiveIntegerField(help_text="Pledge amount")
    message = models.TextField(blank=True, help_text="Optional sponsor message")
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        name = "Anonymous" if self.is_anonymous else self.sponsor.username
        return f"{name} pledged {self.amount:,} to {self.campaign.title}"
