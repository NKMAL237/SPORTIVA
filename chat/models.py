from django.db import models
from django.conf import settings


class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    subject = models.CharField(max_length=200, blank=True, help_text="e.g. Sponsorship Query, Event Coordination")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def get_other_participant(self, current_user):
        """Returns the other user in a 1-on-1 conversation."""
        return self.participants.exclude(id=current_user.id).first()

    def latest_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def __str__(self):
        p_names = ", ".join([u.username for u in self.participants.all()[:2]])
        return f"Chat between: {p_names}"


class ChatMessage(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender.username}] {self.content[:30]}"
