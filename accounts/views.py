from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone  # ← ADDED
from .models import User, Follow, AthleteExploit, AthleteEndorsement, sportiva_score_annotation
from .decorators import tab_required


AVAILABLE_SPORTS_LIST = [
    'Football', 'Basketball', 'Athletics', 'Tennis', 'Combat Sports',
    'Volleyball', 'Fitness & Gym', 'Swimming', 'Cycling', 'Rugby', 'Handball'
]


def register_view(request):
    """User registration view with global roles (including Visitor), country, and sport preferences."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', User.Role.ATHLETE)
        country = request.POST.get('country', 'Global').strip() or 'Global'
        city = request.POST.get('city', 'Global City').strip() or 'Global City'
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        selected_sports = request.POST.getlist('favorite_sports')

        if not username or not email or not password:
            messages.error(request, "Username, email, and password are required.")
            return render(request, 'accounts/register.html', {
                'post': request.POST,
                'available_sports': AVAILABLE_SPORTS_LIST
            })

        if password != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'accounts/register.html', {
                'post': request.POST,
                'available_sports': AVAILABLE_SPORTS_LIST
            })

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'accounts/register.html', {
                'post': request.POST,
                'available_sports': AVAILABLE_SPORTS_LIST
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken. Please choose another.")
            return render(request, 'accounts/register.html', {
                'post': request.POST,
                'available_sports': AVAILABLE_SPORTS_LIST
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'accounts/register.html', {
                'post': request.POST,
                'available_sports': AVAILABLE_SPORTS_LIST
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            country=country,
            city=city,
            phone_number=phone_number,
            favorite_sports=selected_sports,
        )
        login(request, user)
        messages.success(request, f"Welcome to SPORTIVA, {user.username}! 🎉 Your global sports journey begins now.")
        return redirect('home')

    return render(request, 'accounts/register.html', {
        'available_sports': AVAILABLE_SPORTS_LIST
    })


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
    """Redirect to user's personal profile view."""
    return redirect('user_detail', username=request.user.username)


def profiles_list_view(request):
    """
    Global Community Profiles Directory:
    Displays athletes, clubs, coaches, sponsors and fans with search, filter, and score tiering.
    """
    search_query = request.GET.get('search', '').strip()
    role_filter = request.GET.get('role', '')
    country_filter = request.GET.get('country', '').strip()
    sport_filter = request.GET.get('sport', '').strip()
    sort_by = request.GET.get('sort', 'score')

    queryset = (
        User.objects.filter(is_active=True)
        .annotate(**sportiva_score_annotation())
        .prefetch_related('followers', 'exploits')
    )

    if search_query:
        queryset = queryset.filter(
            models.Q(username__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(city__icontains=search_query) |
            models.Q(country__icontains=search_query) |
            models.Q(bio__icontains=search_query)
        )

    if role_filter:
        queryset = queryset.filter(role=role_filter)

    if country_filter:
        queryset = queryset.filter(country__icontains=country_filter)

    users_list = list(queryset)

    if sport_filter:
        users_list = [u for u in users_list if sport_filter.lower() in [s.lower() for s in (u.favorite_sports or [])]]

    # Sorting
    if sort_by == 'score':
        users_list.sort(key=lambda u: u.sportiva_score, reverse=True)
    elif sort_by == 'followers':
        users_list.sort(key=lambda u: u.followers.count(), reverse=True)
    elif sort_by == 'newest':
        users_list.sort(key=lambda u: u.date_joined, reverse=True)

    # Top featured athletes leaderboard
    top_athletes = list(
        User.objects.filter(role=User.Role.ATHLETE, is_active=True)
        .annotate(**sportiva_score_annotation())
        .order_by('-_sportiva_score')[:5]
    )

    followed_ids = (
        set(request.user.following.values_list('followed_user_id', flat=True))
        if request.user.is_authenticated else set()
    )

    context = {
        'profiles': users_list,
        'top_athletes': top_athletes,
        'followed_ids': followed_ids,
        'search_query': search_query,
        'role_filter': role_filter,
        'country_filter': country_filter,
        'sport_filter': sport_filter,
        'sort_by': sort_by,
        'roles': User.Role.choices,
        'available_sports': AVAILABLE_SPORTS_LIST,
    }
    return render(request, 'accounts/profiles_list.html', context)


def user_detail_view(request, username):
    """
    Public Profile View:
    Showcases athlete exploits, verified scoring, social links, sponsor profile, and follow action.
    """
    profile_user = get_object_or_404(User, username=username)
    from events.models import EventAttendance
    from media_feed.models import Post
    from organizations.models import OrganizationProfile

    # Exploits
    if request.user.is_authenticated and (request.user == profile_user or request.user.role in [User.Role.ORGANIZATION, User.Role.TRAINER, User.Role.SPONSOR] or request.user.is_staff):
        exploits = profile_user.exploits.all()
    else:
        exploits = profile_user.exploits.filter(status='VERIFIED')

    verified_count = profile_user.exploits.filter(status='VERIFIED').count()
    pending_count = profile_user.exploits.filter(status='PENDING').count()

    is_following = profile_user.is_followed_by(request.user) if request.user.is_authenticated else False

    # Check if current user can verify exploits (Coach, Club, Sponsor, Organizer, Staff)
    can_verify = (
        request.user.is_authenticated and
        request.user != profile_user and
        (request.user.role in [User.Role.ORGANIZATION, User.Role.TRAINER, User.Role.SPONSOR] or request.user.is_staff or request.user.is_superuser)
    )

    # Organization or Sponsor Profile if exists
    org_profile = OrganizationProfile.objects.filter(user=profile_user).first()
    
    sponsor_profile = None
    if hasattr(profile_user, 'sponsor_profile'):
        sponsor_profile = profile_user.sponsor_profile

    context = {
        'profile_user': profile_user,
        'exploits': exploits,
        'verified_count': verified_count,
        'pending_count': pending_count,
        'endorsements': profile_user.endorsements.all(),
        'is_following': is_following,
        'can_verify': can_verify,
        'events_attended': EventAttendance.objects.filter(user=profile_user).count(),
        'posts_count': Post.objects.filter(author=profile_user).count(),
        'recent_posts': Post.objects.filter(author=profile_user)[:4],
        'org_profile': org_profile,
        'sponsor_profile': sponsor_profile,
        'is_owner': request.user == profile_user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit current user's profile, bio, avatar, social handles and sports preferences."""
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()
        user.country = request.POST.get('country', user.country).strip()
        user.city = request.POST.get('city', user.city).strip()
        user.phone_number = request.POST.get('phone_number', user.phone_number).strip()
        user.bio = request.POST.get('bio', user.bio).strip()
        
        # Social links
        user.telegram = request.POST.get('telegram', user.telegram).strip()
        user.instagram = request.POST.get('instagram', user.instagram).strip()
        user.twitter = request.POST.get('twitter', user.twitter).strip()
        user.linkedin = request.POST.get('linkedin', user.linkedin).strip()
        user.tiktok = request.POST.get('tiktok', user.tiktok).strip()
        user.youtube = request.POST.get('youtube', user.youtube).strip()

        # Favorite sports
        user.favorite_sports = request.POST.getlist('favorite_sports')

        # Avatar upload
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, "Your SPORTIVA profile has been updated successfully!")
        return redirect('user_detail', username=user.username)

    return render(request, 'accounts/profile_edit.html', {
        'available_sports': AVAILABLE_SPORTS_LIST
    })


@login_required
@require_POST
def toggle_follow_view(request, user_id):
    """Toggle follow/subscribe for an athlete, club, sponsor, or user."""
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('user_detail', username=target_user.username)

    follow_obj = Follow.objects.filter(follower=request.user, followed_user=target_user).first()
    if follow_obj:
        follow_obj.delete()
        messages.info(request, f"You have unfollowed {target_user.username}.")
    else:
        Follow.objects.create(follower=request.user, followed_user=target_user)
        messages.success(request, f"You are now following {target_user.username}! 🌟")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or f"/accounts/profile/{target_user.username}/"
    return redirect(next_url)


@login_required
def add_exploit_view(request):
    """Allows an athlete to add their exploits, merits and achievements for verification."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'MEDAL')
        competition_name = request.POST.get('competition_name', '').strip()
        date_achieved = request.POST.get('date_achieved')
        description = request.POST.get('description', '').strip()
        proof_link = request.POST.get('proof_link', '').strip()
        proof_image = request.FILES.get('proof_image')

        if not title or not competition_name:
            messages.error(request, "Title and competition/event name are required.")
            return render(request, 'accounts/exploit_form.html', {
                'categories': AthleteExploit.CATEGORY_CHOICES
            })

        exploit = AthleteExploit.objects.create(
            athlete=request.user,
            title=title,
            category=category,
            competition_name=competition_name,
            date_achieved=date_achieved if date_achieved else timezone.now().date(),
            description=description,
            proof_link=proof_link,
            proof_image=proof_image,
            status='PENDING'
        )

        messages.success(
            request,
            f"Exploit '{exploit.title}' added successfully! It is now pending validation by a certified Coach, Club, Sponsor, or Organizer."
        )
        return redirect('user_detail', username=request.user.username)

    return render(request, 'accounts/exploit_form.html', {
        'categories': AthleteExploit.CATEGORY_CHOICES
    })


@login_required
def edit_exploit_view(request, exploit_id):
    """Allows athlete to edit an existing exploit or see review feedback."""
    exploit = get_object_or_404(AthleteExploit, id=exploit_id)
    if exploit.athlete != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to edit this exploit.")
        return redirect('user_detail', username=exploit.athlete.username)

    if request.method == 'POST':
        exploit.title = request.POST.get('title', exploit.title).strip()
        exploit.category = request.POST.get('category', exploit.category)
        exploit.competition_name = request.POST.get('competition_name', exploit.competition_name).strip()
        if request.POST.get('date_achieved'):
            exploit.date_achieved = request.POST.get('date_achieved')
        exploit.description = request.POST.get('description', exploit.description).strip()
        exploit.proof_link = request.POST.get('proof_link', exploit.proof_link).strip()
        if 'proof_image' in request.FILES:
            exploit.proof_image = request.FILES['proof_image']

        exploit.status = 'PENDING'  # reset to pending after major edits
        exploit.save()

        messages.success(request, f"Exploit '{exploit.title}' updated and submitted for verification.")
        return redirect('user_detail', username=request.user.username)

    return render(request, 'accounts/exploit_form.html', {
        'exploit': exploit,
        'categories': AthleteExploit.CATEGORY_CHOICES
    })


@login_required
def verify_exploit_view(request, exploit_id):
    """
    Verification Endpoint:
    Allows coaches, clubs, organizers, and sponsors to validate or reject an athlete exploit.
    """
    exploit = get_object_or_404(AthleteExploit, id=exploit_id)
    
    # Check authorization
    if request.user == exploit.athlete:
        messages.error(request, "You cannot validate your own exploit. A coach, club, organizer, or sponsor must validate it.")
        return redirect('user_detail', username=exploit.athlete.username)

    if not (request.user.role in [User.Role.ORGANIZATION, User.Role.TRAINER, User.Role.SPONSOR] or request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Only coaches, club managers, event organizers, or sponsors can validate athlete exploits.")
        return redirect('user_detail', username=exploit.athlete.username)

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('validation_notes', '').strip()
        points = int(request.POST.get('score_points', 35))

        if action == 'VERIFY':
            exploit.status = 'VERIFIED'
            exploit.validated_by = request.user
            exploit.validation_notes = notes
            exploit.score_points = points
            exploit.save()
            messages.success(
                request,
                f"Exploit '{exploit.title}' successfully verified! Added {points} points to {exploit.athlete.username}'s Sportiva Score."
            )
        elif action == 'REJECT':
            exploit.status = 'REJECTED'
            exploit.validated_by = request.user
            exploit.validation_notes = notes
            exploit.save()
            messages.warning(request, f"Exploit '{exploit.title}' marked as unverified/rejected.")

    return redirect('user_detail', username=exploit.athlete.username)


@login_required
@require_POST
def endorse_athlete_view(request, athlete_id):
    """Add a skill endorsement from a coach, teammate, or fan."""
    athlete = get_object_or_404(User, id=athlete_id)
    if athlete == request.user:
        messages.error(request, "You cannot endorse yourself.")
        return redirect('user_detail', username=athlete.username)

    skill = request.POST.get('skill_or_merit', '').strip()
    comment = request.POST.get('comment', '').strip()

    if skill:
        AthleteEndorsement.objects.update_or_create(
            athlete=athlete,
            endorsed_by=request.user,
            skill_or_merit=skill,
            defaults={'comment': comment}
        )
        messages.success(request, f"You endorsed {athlete.username} for '{skill}'! (+10 Sportiva Merit Score)")

    return redirect('user_detail', username=athlete.username)


@login_required
@tab_required('user_management')
def user_management_view(request):
    """User Management Dashboard: Lists all users and manages tab access permissions."""
    search_query = request.GET.get('search', '').strip()
    role_filter = request.GET.get('role', '')

    queryset = User.objects.all().annotate(**sportiva_score_annotation()).order_by('-date_joined')

    if search_query:
        queryset = queryset.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(city__icontains=search_query) |
            models.Q(country__icontains=search_query)
        )
    if role_filter:
        queryset = queryset.filter(role=role_filter)

    users_with_tabs = []
    for u in queryset:
        users_with_tabs.append({
            'user_obj': u,
            'allowed_tabs': u.get_allowed_tabs(),
            'custom_overrides': u.custom_allowed_tabs or {},
            'score': u.sportiva_score,
            'tier': u.sportiva_tier,
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
    """Updates role, active status, and custom tab permissions for a specific user."""
    target_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role', target_user.role)
        is_active = request.POST.get('is_active') == 'on'
        is_verified = request.POST.get('is_verified') == 'on'

        new_custom_tabs = {}
        for tab_key, _ in User.ALL_TABS:
            field_name = f"tab_{tab_key}"
            new_custom_tabs[tab_key] = field_name in request.POST

        target_user.role = new_role
        target_user.is_active = is_active
        target_user.is_verified = is_verified
        target_user.custom_allowed_tabs = new_custom_tabs
        target_user.save()

        messages.success(
            request,
            f"Permissions updated successfully for user '{target_user.username}'."
        )

    return redirect('user_management')