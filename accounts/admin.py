from django.contrib import admin
from .models import User, Follow, AthleteExploit, AthleteEndorsement


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'city', 'country', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'city', 'country', 'is_verified', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'city', 'country']
    list_editable = ['is_verified', 'is_active']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'followed_user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'followed_user__username']


@admin.register(AthleteExploit)
class AthleteExploitAdmin(admin.ModelAdmin):
    list_display = ['title', 'athlete', 'category', 'status', 'score_points', 'date_achieved', 'validated_by']
    list_filter = ['status', 'category', 'date_achieved']
    search_fields = ['title', 'competition_name', 'athlete__username']
    list_editable = ['status', 'score_points']


@admin.register(AthleteEndorsement)
class AthleteEndorsementAdmin(admin.ModelAdmin):
    list_display = ['athlete', 'endorsed_by', 'skill_or_merit', 'created_at']
    list_filter = ['created_at']
    search_fields = ['athlete__username', 'endorsed_by__username', 'skill_or_merit']