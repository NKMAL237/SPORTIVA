from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Campaign, Pledge


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'category', 'description', 'target_amount', 'city', 'deadline', 'banner', 'whatsapp_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'target_amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'Amount in FCFA'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': '+237699000000'}),
        }


class PledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = ['amount', 'message', 'is_anonymous']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'Amount in FCFA'}),
            'message': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'Optional support message...'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'rounded border-slate-600 bg-slate-900 text-emerald-500'}),
        }


def sponsorships_list(request):
    """List all active sponsorship campaigns."""
    city_filter = request.GET.get('city', '')
    cat_filter = request.GET.get('category', '')

    queryset = Campaign.objects.filter(is_active=True).select_related('creator')

    if city_filter:
        queryset = queryset.filter(city=city_filter)
    if cat_filter:
        queryset = queryset.filter(category=cat_filter)

    context = {
        'campaigns': queryset,
        'categories': Campaign.CATEGORY_CHOICES,
        'selected_city': city_filter,
        'selected_category': cat_filter,
    }
    return render(request, 'sponsorships/list.html', context)


def campaign_detail(request, pk):
    """Campaign detail with pledge form and donor list."""
    campaign = get_object_or_404(Campaign.objects.select_related('creator'), pk=pk, is_active=True)
    pledges = campaign.pledges.select_related('sponsor').all()
    pledge_form = PledgeForm()

    if request.method == 'POST' and request.user.is_authenticated:
        pledge_form = PledgeForm(request.POST)
        if pledge_form.is_valid():
            pledge = pledge_form.save(commit=False)
            pledge.campaign = campaign
            pledge.sponsor = request.user
            pledge.save()
            # Update campaign raised amount
            total = sum(p.amount for p in campaign.pledges.all())
            campaign.raised_amount = total
            campaign.save()
            messages.success(request, f"Thank you for pledging {pledge.amount:,} FCFA to '{campaign.title}'! 🙌")
            return redirect('campaign_detail', pk=pk)
    elif request.method == 'POST':
        messages.error(request, "Please log in to make a pledge.")
        return redirect('login')

    context = {
        'campaign': campaign,
        'pledges': pledges,
        'pledge_form': pledge_form,
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
