from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_inbox_view, name='chat_inbox'),
    path('<int:conversation_id>/', views.chat_inbox_view, name='chat_conversation'),
    path('start/<int:user_id>/', views.start_direct_chat, name='start_direct_chat'),
    path('start-chat/<int:user_id>/', views.start_direct_chat, name='chat_start'),
]
