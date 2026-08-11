from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Product, ProductCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'condition', 'city', 'image', 'whatsapp_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'Price in FCFA'}),
            'condition': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': '+237699000000'}),
        }


def marketplace_list(request):
    """List available sports equipment for sale."""
    city_filter = request.GET.get('city', '')
    cat_filter = request.GET.get('category', '')
    condition_filter = request.GET.get('condition', '')

    queryset = Product.objects.filter(is_available=True).select_related('seller', 'category')

    if city_filter:
        queryset = queryset.filter(city=city_filter)
    if cat_filter:
        queryset = queryset.filter(category__id=cat_filter)
    if condition_filter:
        queryset = queryset.filter(condition=condition_filter)

    categories = ProductCategory.objects.all()

    context = {
        'products': queryset,
        'categories': categories,
        'conditions': Product.CONDITION_CHOICES,
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
