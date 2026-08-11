from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'city', 'is_verified', 'date_joined']
    list_filter = ['role', 'city', 'is_verified', 'is_staff']
    search_fields = ['username', 'email', 'city']
