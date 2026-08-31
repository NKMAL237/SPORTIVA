from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User


def register_view(request):
    """User registration view with role, city, and WhatsApp fields."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', User.Role.ATHLETE)
        city = request.POST.get('city', 'Yaoundé')
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password:
            messages.error(request, "Username, email, and password are required.")
            return render(request, 'accounts/register.html', {'post': request.POST})

        if password != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'accounts/register.html', {'post': request.POST})

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'accounts/register.html', {'post': request.POST})

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken. Please choose another.")
            return render(request, 'accounts/register.html', {'post': request.POST})

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'accounts/register.html', {'post': request.POST})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            city=city,
            phone_number=phone_number,
        )
        login(request, user)
        messages.success(request, f"Welcome to Sportiva CM, {user.username}! 🎉 Your account has been created.")
        return redirect('home')

    return render(request, 'accounts/register.html')


def login_view(request):
    """Login view supporting username/email authentication."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html')


@login_required
def profile_view(request):
    """User profile page with stats."""
    from events.models import EventAttendance
    from media_feed.models import Post
    from organizations.models import OrganizationProfile

    user = request.user
    context = {
        'user': user,
        'events_attended': EventAttendance.objects.filter(user=user).count(),
        'posts_count': Post.objects.filter(author=user).count(),
        'has_organization': OrganizationProfile.objects.filter(user=user).exists(),
        'organization': OrganizationProfile.objects.filter(user=user).first(),
        'recent_posts': Post.objects.filter(author=user)[:3],
    }
    return render(request, 'accounts/profile.html', context)


from .decorators import tab_required
from django.shortcuts import get_object_or_404


@login_required
@tab_required('user_management')
def user_management_view(request):
    """
    User Management Dashboard:
    Lists all users, supports filtering by role and search,
    and displays active tab permissions for each user.
    """
    search_query = request.GET.get('search', '').strip()
    role_filter = request.GET.get('role', '')

    queryset = User.objects.all().order_by('-date_joined')

    if search_query:
        queryset = queryset.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(city__icontains=search_query)
        )
    if role_filter:
        queryset = queryset.filter(role=role_filter)

    # Attach computed allowed_tabs for UI rendering
    users_with_tabs = []
    for u in queryset:
        users_with_tabs.append({
            'user_obj': u,
            'allowed_tabs': u.get_allowed_tabs(),
            'custom_overrides': u.custom_allowed_tabs or {},
        })

    all_tabs = User.ALL_TABS
    roles = User.Role.choices

    context = {
        'users_data': users_with_tabs,
        'all_tabs': all_tabs,
        'roles': roles,
        'search_query': search_query,
        'selected_role': role_filter,
    }
    return render(request, 'accounts/user_management.html', context)


@login_required
@tab_required('user_management')
def user_update_tabs_view(request, user_id):
    """
    Updates role and custom tab access permissions for a specific user.
    """
    target_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role', target_user.role)
        is_active = request.POST.get('is_active') == 'on'

        # Build custom allowed tabs dict from form checkboxes
        new_custom_tabs = {}
        for tab_key, _ in User.ALL_TABS:
            field_name = f"tab_{tab_key}"
            if field_name in request.POST:
                new_custom_tabs[tab_key] = True
            else:
                new_custom_tabs[tab_key] = False

        target_user.role = new_role
        target_user.is_active = is_active
        target_user.custom_allowed_tabs = new_custom_tabs
        target_user.save()

        messages.success(
            request,
            f"Permissions updated successfully for user '{target_user.username}'."
        )

    return redirect('user_management')

