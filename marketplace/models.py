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
    CITY_CHOICES = [
        ('Yaoundé', 'Yaoundé'),
        ('Douala', 'Douala'),
        ('Bafoussam', 'Bafoussam'),
        ('Garoua', 'Garoua'),
        ('Bamenda', 'Bamenda'),
        ('Buea', 'Buea'),
        ('Maroua', 'Maroua'),
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
    price = models.PositiveIntegerField(help_text="Price in FCFA")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='GOOD')
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default='Yaoundé')
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean_whatsapp(self):
        if not self.whatsapp_number:
            return ""
        digits = "".join([c for c in self.whatsapp_number if c.isdigit()])
        if not digits.startswith("237") and len(digits) == 9:
            digits = "237" + digits
        return digits

    def price_formatted(self):
        return f"{self.price:,} FCFA"

    def __str__(self):
        return f"{self.title} — {self.price_formatted()} ({self.city})"
