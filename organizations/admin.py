from django.contrib import admin
from .models import SportsCategory, OrganizationProfile


@admin.register(SportsCategory)
class SportsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class', 'description']
    search_fields = ['name']


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'sports_category', 'city', 'country', 'is_verified', 'created_at']
    list_filter = ['sports_category', 'city', 'country', 'is_verified']
    search_fields = ['name', 'user__username', 'description']
    list_editable = ['is_verified']