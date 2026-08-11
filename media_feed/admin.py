from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'city', 'is_published', 'created_at']
    list_filter = ['post_type', 'city', 'is_published']
    search_fields = ['content', 'title', 'author__username']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']

admin.site.register(Like)
