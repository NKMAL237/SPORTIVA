from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ATHLETE = 'ATHLETE', 'Athlete / Sports Enthusiast'
        ORGANIZATION = 'ORGANIZATION', 'Club / Academy / Organization / Manager'
        TRAINER = 'TRAINER', 'Coach / Personal Trainer'
        SPONSOR = 'SPONSOR', 'Sponsor / Business Partner'
        VISITOR = 'VISITOR', 'Visitor / Fan / Supporter'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ATHLETE,
        help_text="Primary role on Sportiva"
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="Direct phone / WhatsApp contact (with country code, e.g., +1..., +33..., +237...)"
    )
    country = models.CharField(
        max_length=100,
        default='Global',
        help_text="Country of residence / operations"
    )
    city = models.CharField(
        max_length=100,
        default='Global City',
        help_text="City of residence / operations"
    )
    bio = models.TextField(
        blank=True,
        help_text="Bio, athletic achievements or organizational overview"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile image / Avatar"
    )
    favorite_sports = models.JSONField(
        default=list,
        blank=True,
        help_text="List of favorite sports/disciplines chosen by the user (e.g. ['Football', 'Basketball'])"
    )
    
    # Social Network Connections
    telegram = models.CharField(max_length=100, blank=True, help_text="Telegram username or link (@username or t.me/...)")
    instagram = models.CharField(max_length=100, blank=True, help_text="Instagram handle or link (@username or instagram.com/...)")
    twitter = models.CharField(max_length=100, blank=True, help_text="Twitter/X handle or link (@username or x.com/...)")
    linkedin = models.CharField(max_length=200, blank=True, help_text="LinkedIn profile link")
    tiktok = models.CharField(max_length=100, blank=True, help_text="TikTok handle (@username)")
    youtube = models.CharField(max_length=200, blank=True, help_text="YouTube channel or link")

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
        ('profiles', 'Profiles'),
        ('events', 'Events'),
        ('organizations', 'Organizations'),
        ('media_feed', 'News & Feed'),
        ('marketplace', 'Marketplace'),
        ('sponsorships', 'Sponsorships'),
        ('chat', 'Chat'),
        ('user_management', 'User Management'),
    ]

    DEFAULT_ROLE_TABS = {
        Role.ATHLETE: ['home', 'profiles', 'events', 'media_feed', 'marketplace', 'sponsorships', 'chat'],
        Role.ORGANIZATION: ['home', 'profiles', 'events', 'organizations', 'media_feed', 'sponsorships', 'marketplace', 'chat'],
        Role.TRAINER: ['home', 'profiles', 'events', 'organizations', 'media_feed', 'marketplace', 'chat'],
        Role.SPONSOR: ['home', 'profiles', 'events', 'organizations', 'media_feed', 'sponsorships', 'chat'],
        Role.VISITOR: ['home', 'profiles', 'events', 'media_feed', 'marketplace', 'chat'],
    }

    def get_allowed_tabs(self):
        """Returns list of tab keys that this user is allowed to access."""
        all_tab_keys = [t[0] for t in self.ALL_TABS]
        if self.is_superuser or self.is_staff:
            return all_tab_keys

        default_tabs = set(self.DEFAULT_ROLE_TABS.get(self.role, ['home', 'profiles', 'events', 'media_feed', 'chat']))
        
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
        return "".join([c for c in self.phone_number if c.isdigit()])

    def clean_social_link(self, network):
        val = getattr(self, network, '').strip()
        if not val:
            return ""
        if val.startswith('http://') or val.startswith('https://'):
            return val
        clean_handle = val.lstrip('@')
        if network == 'telegram':
            return f"https://t.me/{clean_handle}"
        elif network == 'instagram':
            return f"https://instagram.com/{clean_handle}"
        elif network == 'twitter':
            return f"https://x.com/{clean_handle}"
        elif network == 'tiktok':
            return f"https://tiktok.com/@{clean_handle}"
        return val

    @property
    def sportiva_score(self):
        """Calculates global merit score for athlete/user based on verified exploits and activity."""
        base_score = 50
        # Add points from verified exploits
        verified_exploits = self.exploits.filter(status='VERIFIED')
        exploit_points = sum(e.score_points for e in verified_exploits)
        
        # Add points from followers
        follower_points = self.followers.count() * 5
        
        # Add points from endorsements
        endorsement_points = self.endorsements.count() * 10
        
        # Event attendances
        attendance_points = self.event_attendances.count() * 15 if hasattr(self, 'event_attendances') else 0

        return base_score + exploit_points + follower_points + endorsement_points + attendance_points

    @property
    def sportiva_tier(self):
        score = self.sportiva_score
        if score >= 500:
            return {"name": "Legendary", "badge": "🏆", "color": "text-amber-400 bg-amber-500/10 border-amber-500/30", "bar_width": 100}
        elif score >= 250:
            return {"name": "Elite", "badge": "⚡", "color": "text-purple-400 bg-purple-500/10 border-purple-500/30", "bar_width": 75}
        elif score >= 120:
            return {"name": "Pro", "badge": "⭐", "color": "text-cyan-400 bg-cyan-500/10 border-cyan-500/30", "bar_width": 50}
        else:
            return {"name": "Rising Star", "badge": "🚀", "color": "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", "bar_width": 25}

    def is_followed_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.followers.filter(follower=user).exists()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.followed_user.username}"


class AthleteExploit(models.Model):
    CATEGORY_CHOICES = [
        ('TITLE', 'Tournament / Championship Title'),
        ('MEDAL', 'Medal / Podium (Gold/Silver/Bronze)'),
        ('MVP', 'MVP / Best Player Award'),
        ('RECORD', 'Record / Personal Best / Exploit'),
        ('MATCH_WIN', 'Decisive Match / Tournament Victory'),
        ('CAPTAINCY', 'Captaincy / Leadership Exploit'),
        ('OTHER', 'Honor / Sports Achievement'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Verified & Validated'),
        ('REJECTED', 'Rejected'),
    ]

    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exploits')
    title = models.CharField(max_length=200, help_text="e.g., Top Scorer Champion's Cup 2026, 100m Gold Medalist")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='MEDAL')
    competition_name = models.CharField(max_length=200, help_text="e.g. World Youth Games, National Championship")
    date_achieved = models.DateField(default=timezone.now)
    description = models.TextField(help_text="Details of the exploit, statistics, records, or match impact")
    proof_image = models.ImageField(upload_to='exploits/', blank=True, null=True, help_text="Certificate, medal photo, or scoresheet")
    proof_link = models.URLField(blank=True, help_text="Official results link or video evidence")
    
    # Verification system
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    validated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_exploits',
        help_text="Coach, Club, Sponsor, or Organizer who verified this exploit"
    )
    validation_notes = models.TextField(blank=True, help_text="Verification verdict and notes from validating entity")
    score_points = models.PositiveIntegerField(default=35, help_text="Merit score points granted upon verification")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_achieved', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.athlete.username} ({self.get_status_display()})"


class AthleteEndorsement(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='endorsements')
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_endorsements')
    skill_or_merit = models.CharField(max_length=100, help_text="e.g. Tactical Vision, Speed, Leadership, Fair Play")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('athlete', 'endorsed_by', 'skill_or_merit')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.endorsed_by.username} endorsed {self.athlete.username} for {self.skill_or_merit}"
