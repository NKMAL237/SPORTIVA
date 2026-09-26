from django.contrib import admin
from .models import EventCategory, Event, EventRegistration


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'sport', 'city', 'country', 'start_date', 'entry_fee', 'max_participants', 'is_published']
    list_filter = ['sport', 'category', 'city', 'country', 'is_published', 'start_date']
    search_fields = ['title', 'description', 'venue_name', 'city', 'country']
    list_editable = ['is_published']
    date_hierarchy = 'start_date'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'payment_status', 'amount_paid', 'currency', 'invoice_number', 'registered_at']
    list_filter = ['status', 'payment_status', 'currency', 'registered_at']
    search_fields = ['user__username', 'event__title', 'invoice_number']
    readonly_fields = ['registration_code', 'registered_at']