from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from accounts.models import User
from .models import Conversation, ChatMessage


@login_required
def chat_inbox_view(request, conversation_id=None):
    """
    Split-Screen Chat Inbox:
    Shows all user conversations on the left and the active message thread on the right.
    """
    conversations = request.user.conversations.all().prefetch_related('participants', 'messages')
    
    active_conversation = None
    if conversation_id:
        active_conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    elif conversations.exists():
        active_conversation = conversations.first()

    # Handle new message submission
    if request.method == 'POST' and active_conversation:
        content = request.POST.get('content', '').strip()
        attachment = request.FILES.get('attachment')
        if content or attachment:
            msg = ChatMessage.objects.create(
                conversation=active_conversation,
                sender=request.user,
                content=content,
                attachment=attachment
            )
            active_conversation.save()  # update updated_at timestamp
            return redirect('chat:chat_conversation', conversation_id=active_conversation.id)

    # Mark unread messages as read
    if active_conversation:
        active_conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    chat_data = []
    for c in conversations:
        other_user = c.get_other_participant(request.user)
        chat_data.append({
            'conversation': c,
            'other_user': other_user,
            'latest_message': c.latest_message(),
            'unread_count': c.unread_count_for(request.user),
            'is_active': active_conversation and c.id == active_conversation.id,
        })

    active_other_user = active_conversation.get_other_participant(request.user) if active_conversation else None
    active_messages = active_conversation.messages.select_related('sender').all() if active_conversation else []

    context = {
        'chat_data': chat_data,
        'active_conversation': active_conversation,
        'active_other_user': active_other_user,
        'active_messages': active_messages,
    }
    return render(request, 'chat/inbox.html', context)


@login_required
def start_direct_chat(request, user_id):
    """
    Finds existing conversation with user or creates a new one, then redirects to chat inbox.
    """
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.warning(request, "You cannot start a chat with yourself.")
        return redirect('chat:chat_inbox')

    # Look for existing 1-on-1 conversation
    existing_conv = Conversation.objects.filter(participants=request.user).filter(participants=target_user).first()
    
    if not existing_conv:
        existing_conv = Conversation.objects.create(subject=f"Chat with {target_user.username}")
        existing_conv.participants.add(request.user, target_user)

    return redirect('chat:chat_conversation', conversation_id=existing_conv.id)
