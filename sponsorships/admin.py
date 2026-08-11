from django.contrib import admin
from .models import Campaign, Pledge

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'target_amount', 'raised_amount', 'city', 'is_active', 'created_at']
    list_filter = ['category', 'city', 'is_active']
    search_fields = ['title', 'creator__username']

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ['sponsor', 'campaign', 'amount', 'is_anonymous', 'created_at']
