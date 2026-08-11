from django.contrib import admin
from .models import ProductCategory, Product

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'condition', 'city', 'is_available', 'created_at']
    list_filter = ['condition', 'city', 'is_available', 'category']
    search_fields = ['title', 'seller__username']
