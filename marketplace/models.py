from django.db import models
from django.conf import settings


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, default='fa-box')

    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'Brand New'),
        ('LIKE_NEW', 'Like New'),
        ('GOOD', 'Good Condition'),
        ('FAIR', 'Fair Condition'),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="Price in local or selected currency")
    currency = models.CharField(max_length=10, default='USD', help_text="USD, EUR, FCFA, GBP")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='GOOD')
    country = models.CharField(max_length=100, default='Global')
    city = models.CharField(max_length=100, default='Global City')
    latitude = models.FloatField(default=3.8864, help_text="GPS Latitude")
    longitude = models.FloatField(default=11.5367, help_text="GPS Longitude")
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean_whatsapp(self):
        if not self.whatsapp_number:
            return ""
        return "".join([c for c in self.whatsapp_number if c.isdigit()])

    def price_formatted(self):
        return f"{self.price:,} {self.currency}"

    def __str__(self):
        return f"{self.title} — {self.price_formatted()} ({self.city}, {self.country})"
