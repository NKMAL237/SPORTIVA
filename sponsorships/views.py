import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.db import models
from django.utils import timezone
from accounts.decorators import tab_required
from accounts.models import User
from .models import Campaign, Pledge, SponsorProfile, SponsorshipRequest, SponsorshipContract


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'category', 'description', 'target_amount', 'country', 'city', 'deadline', 'banner', 'whatsapp_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'target_amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': 'Amount in USD/EUR/FCFA'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': '+1234567890'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['country', 'city', 'deadline', 'banner', 'whatsapp_number']:
            if field_name in self.fields:
                self.fields[field_name].required = False


class SponsorProfileForm(forms.ModelForm):
    class Meta:
        model = SponsorProfile
        fields = ['company_name', 'brand_tagline', 'industry', 'annual_budget_range', 'what_we_offer', 'requirements_criteria', 'website', 'country', 'city', 'address', 'latitude', 'longitude', 'contact_email', 'whatsapp_number', 'logo']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'brand_tagline': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'industry': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'annual_budget_range': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'what_we_offer': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'requirements_criteria': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'contact_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm'}),
        }


@tab_required('sponsorships')
def sponsorships_list(request):
    """
    Global Sponsorship Hub:
    Displays Crowdfunding Campaigns, Verified Sponsors Directory, and Active Partnerships.
    """
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '')
    tab = request.GET.get('tab', 'sponsors')  # sponsors, campaigns, contracts

    campaigns = Campaign.objects.filter(is_active=True).select_related('creator')
    sponsors = SponsorProfile.objects.all().select_related('user')
    contracts = SponsorshipContract.objects.filter(status='ACTIVE').select_related('sponsor', 'athlete', 'event')

    if search_query:
        campaigns = campaigns.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(city__icontains=search_query) |
            models.Q(country__icontains=search_query)
        )
        sponsors = sponsors.filter(
            models.Q(company_name__icontains=search_query) |
            models.Q(industry__icontains=search_query) |
            models.Q(what_we_offer__icontains=search_query) |
            models.Q(country__icontains=search_query)
        )

    if category_filter:
        campaigns = campaigns.filter(category=category_filter)

    # User proposals if logged in
    user_proposals = []
    if request.user.is_authenticated:
        user_proposals = SponsorshipRequest.objects.filter(
            models.Q(sender=request.user) |
            models.Q(recipient_sponsor=request.user) |
            models.Q(recipient_athlete=request.user)
        ).select_related('sender', 'recipient_sponsor', 'recipient_athlete', 'event')[:5]

    context = {
        'sponsors': sponsors,
        'campaigns': campaigns,
        'contracts': contracts,
        'user_proposals': user_proposals,
        'categories': Campaign.CATEGORY_CHOICES,
        'active_tab': tab,
        'search_query': search_query,
    }
    return render(request, 'sponsorships/list.html', context)


def sponsor_detail_view(request, pk):
    """Dedicated Sponsor Profile view showcasing portfolio, perks, active contracts, and proposal trigger."""
    sponsor = get_object_or_404(SponsorProfile.objects.select_related('user'), pk=pk)
    active_contracts = SponsorshipContract.objects.filter(sponsor=sponsor.user, status='ACTIVE').select_related('athlete', 'event')

    context = {
        'sponsor': sponsor,
        'contracts': active_contracts,
        'is_owner': request.user == sponsor.user if request.user.is_authenticated else False,
    }
    return render(request, 'sponsorships/sponsor_detail.html', context)


@login_required
def sponsor_profile_edit(request):
    """Create or edit current sponsor's company profile."""
    profile, created = SponsorProfile.objects.get_or_create(
        user=request.user,
        defaults={'company_name': request.user.username}
    )

    if request.method == 'POST':
        form = SponsorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            sponsor_prof = form.save(commit=False)
            sports_supported = request.POST.getlist('sports_supported')
            sponsor_prof.sports_supported = sports_supported
            sponsor_prof.save()
            messages.success(request, "Sponsor Profile updated successfully!")
            return redirect('sponsor_detail', pk=sponsor_prof.pk)
    else:
        form = SponsorProfileForm(instance=profile)

    return render(request, 'sponsorships/sponsor_edit.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def send_sponsorship_proposal(request):
    """
    Bidirectional Sponsorship Request View:
    Allows athletes/clubs to request sponsorship from a sponsor,
    OR sponsors to offer partnership deals to athletes/events.
    """
    recipient_sponsor_id = request.GET.get('sponsor_id')
    recipient_athlete_id = request.GET.get('athlete_id')
    event_id = request.GET.get('event_id')

    target_sponsor = User.objects.filter(id=recipient_sponsor_id).first() if recipient_sponsor_id else None
    target_athlete = User.objects.filter(id=recipient_athlete_id).first() if recipient_athlete_id else None

    from events.models import Event
    target_event = Event.objects.filter(id=event_id).first() if event_id else None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        proposal_type = request.POST.get('proposal_type', 'ATHLETE_TO_SPONSOR')
        amount = request.POST.get('amount', '').strip()
        deliverables = request.POST.get('deliverables_description', '').strip()
        perks = request.POST.get('perks_offered', '').strip()
        
        sponsor_uid = request.POST.get('recipient_sponsor_id')
        athlete_uid = request.POST.get('recipient_athlete_id')
        ev_id = request.POST.get('event_id')

        recip_sponsor = User.objects.filter(id=sponsor_uid).first() if sponsor_uid else None
        recip_athlete = User.objects.filter(id=athlete_uid).first() if athlete_uid else None
        ev_obj = Event.objects.filter(id=ev_id).first() if ev_id else None

        if not title or not amount:
            messages.error(request, "Title and amount/valuation are required.")
        else:
            proposal = SponsorshipRequest.objects.create(
                sender=request.user,
                recipient_sponsor=recip_sponsor,
                recipient_athlete=recip_athlete,
                event=ev_obj,
                title=title,
                proposal_type=proposal_type,
                amount=amount,
                deliverables_description=deliverables,
                perks_offered=perks,
                status='PENDING'
            )
            messages.success(request, f"Sponsorship proposal '{proposal.title}' sent successfully! 🎉")
            return redirect('sponsorships_list')

    all_sponsors = User.objects.filter(role=User.Role.SPONSOR)
    all_athletes = User.objects.filter(role__in=[User.Role.ATHLETE, User.Role.ORGANIZATION])

    context = {
        'target_sponsor': target_sponsor,
        'target_athlete': target_athlete,
        'target_event': target_event,
        'all_sponsors': all_sponsors,
        'all_athletes': all_athletes,
    }
    return render(request, 'sponsorships/proposal_form.html', context)


@login_required
def respond_sponsorship_proposal(request, pk):
    """Accept, Decline, or Convert a proposal into an official Contract."""
    proposal = get_object_or_404(SponsorshipRequest, pk=pk)
    
    # Check permissions
    can_respond = (
        request.user == proposal.recipient_sponsor or
        request.user == proposal.recipient_athlete or
        request.user.is_staff
    )

    if not can_respond:
        messages.error(request, "You are not authorized to respond to this proposal.")
        return redirect('sponsorships_list')

    if request.method == 'POST':
        action = request.POST.get('action')
        response_msg = request.POST.get('response_message', '').strip()

        if action == 'ACCEPT':
            proposal.status = 'ACCEPTED'
            proposal.response_message = response_msg
            proposal.save()

            # Create an official Contract
            contract_code = f"SPT-CTR-{timezone.now().year}-{uuid.uuid4().hex[:6].upper()}"
            sponsor_user = proposal.recipient_sponsor if proposal.recipient_sponsor else proposal.sender
            athlete_user = proposal.recipient_athlete if proposal.recipient_athlete else proposal.sender

            SponsorshipContract.objects.create(
                contract_number=contract_code,
                sponsor=sponsor_user,
                athlete=athlete_user if athlete_user.role == User.Role.ATHLETE else None,
                event=proposal.event,
                title=f"Contract: {proposal.title}",
                financial_value=proposal.amount,
                terms_and_conditions=f"{proposal.deliverables_description}\n\nPerks: {proposal.perks_offered}",
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timezone.timedelta(days=365),
                status='ACTIVE',
                sponsor_signed=True,
                beneficiary_signed=True,
            )
            messages.success(request, f"Proposal accepted and official Contract #{contract_code} has been generated! 🤝")

        elif action == 'DECLINE':
            proposal.status = 'DECLINED'
            proposal.response_message = response_msg
            proposal.save()
            messages.info(request, "Proposal has been declined.")

    return redirect('sponsorships_list')


def campaign_detail(request, pk):
    """Campaign detail with pledge form and donor list."""
    campaign = get_object_or_404(Campaign.objects.select_related('creator'), pk=pk, is_active=True)
    pledges = campaign.pledges.select_related('sponsor').all()

    if request.method == 'POST' and request.user.is_authenticated:
        amount = int(request.POST.get('amount', 0))
        message_text = request.POST.get('message', '').strip()
        is_anon = request.POST.get('is_anonymous') == 'on'

        if amount > 0:
            Pledge.objects.create(
                campaign=campaign,
                sponsor=request.user,
                amount=amount,
                message=message_text,
                is_anonymous=is_anon
            )
            campaign.raised_amount = sum(p.amount for p in campaign.pledges.all())
            campaign.save()
            messages.success(request, f"Thank you for pledging {amount:,} to '{campaign.title}'! 🙌")
            return redirect('campaign_detail', pk=pk)
    elif request.method == 'POST':
        messages.error(request, "Please log in to make a pledge.")
        return redirect('login')

    context = {
        'campaign': campaign,
        'pledges': pledges,
        'progress': campaign.progress_percent(),
    }
    return render(request, 'sponsorships/detail.html', context)


@login_required
def campaign_create(request):
    """Create a new sponsorship campaign."""
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.creator = request.user
            campaign.save()
            messages.success(request, f"Campaign '{campaign.title}' published successfully!")
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm()
    return render(request, 'sponsorships/create.html', {'form': form})
