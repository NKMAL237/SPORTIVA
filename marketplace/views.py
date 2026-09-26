from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.db import models
from accounts.decorators import tab_required
from .models import Product, ProductCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'currency', 'condition', 'country', 'city', 'latitude', 'longitude', 'image', 'whatsapp_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': 'Price'}),
            'currency': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': 'USD, EUR, FCFA, GBP'}),
            'condition': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'step': '0.0001'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'step': '0.0001'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': '+1234567890'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['currency', 'country', 'city', 'latitude', 'longitude', 'whatsapp_number', 'image']:
            if field_name in self.fields:
                self.fields[field_name].required = False


@tab_required('marketplace')
def marketplace_list(request):
    """List available sports gear, equipment and items for sale globally."""
    search_query = request.GET.get('search', '').strip()
    country_filter = request.GET.get('country', '').strip()
    city_filter = request.GET.get('city', '').strip()
    cat_filter = request.GET.get('category', '')
    condition_filter = request.GET.get('condition', '')

    queryset = Product.objects.filter(is_available=True).select_related('seller', 'category')

    if search_query:
        queryset = queryset.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(city__icontains=search_query) |
            models.Q(country__icontains=search_query)
        )
    if country_filter:
        queryset = queryset.filter(country__icontains=country_filter)
    if city_filter:
        queryset = queryset.filter(city__icontains=city_filter)
    if cat_filter:
        queryset = queryset.filter(category__id=cat_filter)
    if condition_filter:
        queryset = queryset.filter(condition=condition_filter)

    categories = ProductCategory.objects.all()

    context = {
        'products': queryset,
        'categories': categories,
        'conditions': Product.CONDITION_CHOICES,
        'search_query': search_query,
        'selected_country': country_filter,
        'selected_city': city_filter,
        'selected_category': cat_filter,
        'selected_condition': condition_filter,
    }
    return render(request, 'marketplace/list.html', context)


def product_detail(request, pk):
    """Detailed product listing page."""
    product = get_object_or_404(Product.objects.select_related('seller', 'category'), pk=pk, is_available=True)
    return render(request, 'marketplace/detail.html', {'product': product})


@login_required
def product_create(request):
    """Post a sports item for sale."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f"'{product.title}' listed successfully in the Marketplace!")
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'marketplace/create.html', {'form': form})


@login_required
def product_delete(request, pk):
    """Allows the seller (or staff) to remove their marketplace listing."""
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user and not request.user.is_staff:
        messages.error(request, "You can only delete your own listings.")
        return redirect('product_detail', pk=pk)

    if request.method == 'POST':
        title = product.title
        product.delete()
        messages.warning(request, f"'{title}' has been removed from the Marketplace.")
        return redirect('marketplace_list')

    return render(request, 'marketplace/product_delete_confirm.html', {'product': product})
