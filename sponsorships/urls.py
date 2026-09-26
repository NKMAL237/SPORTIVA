from django.urls import path
from . import views

urlpatterns = [
    path('', views.sponsorships_list, name='sponsorships_list'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:pk>/delete/', views.delete_campaign, name='delete_campaign'),
    path('sponsors/<int:pk>/', views.sponsor_detail_view, name='sponsor_detail'),
    path('sponsors/edit/', views.sponsor_profile_edit, name='sponsor_profile_edit'),
    path('proposals/send/', views.send_sponsorship_proposal, name='send_proposal'),
    path('proposals/<int:pk>/respond/', views.respond_sponsorship_proposal, name='respond_proposal'),
    path('proposals/<int:pk>/withdraw/', views.withdraw_proposal, name='withdraw_proposal'),
    path('pledges/<int:pk>/delete/', views.delete_pledge, name='delete_pledge'),
]
