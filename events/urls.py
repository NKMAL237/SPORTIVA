from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/register-payment/', views.event_register_payment, name='event_register_payment'),
    path('<int:pk>/rsvp/', views.event_register_payment, name='event_rsvp'),
    path('<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('registration/<int:pk>/invoice/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('registration/<int:pk>/validate/', views.validate_registration_view, name='validate_registration'),
    path('registration/<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'),
]
