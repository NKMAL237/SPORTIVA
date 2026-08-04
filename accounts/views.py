from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def register_view(request):
    """Temporary placeholder for User Registration view."""
    return render(request, 'accounts/register.html')

def login_view(request):
    """Temporary placeholder for User Login view."""
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    """User Profile view."""
    return render(request, 'accounts/profile.html', {'user': request.user})
