# apps/qrcodes/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.restaurants.models import QRCode
from apps.menus.models import Category, MenuItem


def public_menu(request, uuid):
    """Page publique - charge les 4 premières catégories."""
    qr_code = get_object_or_404(QRCode, uuid=uuid, is_active=True, restaurant__is_active=True)
    restaurant = qr_code.restaurant
    
    # Toutes les catégories actives
    all_categories = Category.objects.filter(
        restaurant=restaurant,
        is_active=True
    ).order_by('order', 'name')
    
    total_categories = all_categories.count()
    
    # Afficher les 4 premières
    first_categories = all_categories[:4]
    
    # Préparer les données
    categories_with_items = []
    for cat in first_categories:
        items = cat.items.filter(is_available=True).order_by('order', 'name')[:6]
        categories_with_items.append({
            'category': cat,
            'items': items,
            'total_items': cat.items.filter(is_available=True).count(),
        })
    
    theme = {
        'primary': restaurant.primary_color or '#1e40af',
        'secondary': restaurant.secondary_color or '#f59e0b',
        'background': restaurant.background_color or '#f9fafb',
        'text': restaurant.text_color or '#1f2937',
        'header_opacity': float(restaurant.header_opacity) if restaurant.header_opacity else 1.0,
    }
    
    context = {
        'restaurant': restaurant,
        'categories_with_items': categories_with_items,
        'total_categories': total_categories,
        'has_more': total_categories > 4,
        'total_items': MenuItem.objects.filter(
            category__restaurant=restaurant,
            is_available=True,
            category__is_active=True
        ).count(),
        'theme': theme,
        'qr_uuid': uuid,
    }
    
    return render(request, 'qrcodes/public_menu.html', context)


def load_more_categories(request, uuid):
    """API : charge plus de catégories (infinite scroll)."""
    offset = int(request.GET.get('offset', 0))
    limit = 4
    
    qr_code = get_object_or_404(QRCode, uuid=uuid, is_active=True, restaurant__is_active=True)
    restaurant = qr_code.restaurant
    
    categories = Category.objects.filter(
        restaurant=restaurant,
        is_active=True
    ).order_by('order', 'name')[offset:offset + limit]
    
    data = []
    for cat in categories:
        items = cat.items.filter(is_available=True).order_by('order', 'name')[:6]
        data.append({
            'id': cat.id,
            'name': cat.name,
            'description': cat.description or '',
            'item_count': cat.items.filter(is_available=True).count(),
            'items': [
                {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description or '',
                    'price': str(item.price),
                    'image_url': item.image.url if item.image else None,
                    'is_vegetarian': item.is_vegetarian,
                    'is_vegan': item.is_vegan,
                    'is_gluten_free': item.is_gluten_free,
                    'allergens': item.allergens or '',
                }
                for item in items
            ],
        })
    
    has_more = Category.objects.filter(
        restaurant=restaurant,
        is_active=True
    ).count() > offset + limit
    
    return JsonResponse({
        'categories': data,
        'has_more': has_more,
        'next_offset': offset + limit,
    })


def load_category_items(request, uuid, category_id):
    """API : charge tous les plats d'une catégorie."""
    qr_code = get_object_or_404(QRCode, uuid=uuid, is_active=True, restaurant__is_active=True)
    
    items = MenuItem.objects.filter(
        category_id=category_id,
        category__restaurant=qr_code.restaurant,
        is_available=True,
        category__is_active=True
    ).order_by('order', 'name')
    
    data = [
        {
            'id': item.id,
            'name': item.name,
            'description': item.description or '',
            'price': str(item.price),
            'image_url': item.image.url if item.image else None,
            'is_vegetarian': item.is_vegetarian,
            'is_vegan': item.is_vegan,
            'is_gluten_free': item.is_gluten_free,
            'allergens': item.allergens or '',
        }
        for item in items
    ]
    
    return JsonResponse({'items': data})