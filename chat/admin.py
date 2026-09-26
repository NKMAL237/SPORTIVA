from django.contrib import admin
from .models import Conversation, ChatMessage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'participant_list', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['subject', 'participants__username']
    filter_horizontal = ['participants']

    def participant_list(self, obj):
        return ", ".join([u.username for u in obj.participants.all()[:3]])
    participant_list.short_description = 'Participants'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'content']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'