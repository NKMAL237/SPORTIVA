from django import forms
from .models import OrganizationProfile


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = [
            'name', 'sports_category', 'country', 'city', 'address',
            'latitude', 'longitude', 'description', 'logo',
            'phone_number', 'whatsapp_number', 'email', 'website'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'sports_category': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'step': '0.0001'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'step': '0.0001'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
        }
