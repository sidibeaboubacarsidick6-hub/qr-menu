# apps/menus/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ['name', 'price', 'is_available', 'order']
    ordering = ['order', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'item_count', 'is_active', 'order']
    list_filter = ['restaurant', 'is_active']
    search_fields = ['name', 'restaurant__name']
    inlines = [MenuItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Nombre de plats"


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'restaurant_name', 'price', 'is_available', 'image_preview']
    list_filter = ['category__restaurant', 'category', 'is_available', 'is_vegetarian', 'is_vegan', 'is_gluten_free']
    search_fields = ['name', 'description', 'category__name']

    def restaurant_name(self, obj):
        return obj.category.restaurant.name
    restaurant_name.short_description = "Restaurant"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "—"
    image_preview.short_description = "Photo"