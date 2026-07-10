from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Restaurant, QRCode
from apps.menus.models import Category, MenuItem


def login_view(request):
    if request.user.is_authenticated:
        return redirect('restaurants:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if hasattr(user, 'restaurant'):
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect('restaurants:dashboard')
            else:
                messages.error(request, "Ce compte n'est pas associé à un restaurant.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'restaurants/login.html')


@login_required
def dashboard(request):
    try:
        restaurant = request.user.restaurant
    except Restaurant.DoesNotExist:
        messages.error(request, "Aucun restaurant associé à votre compte. Contactez l'administrateur.")
        return redirect('restaurants:login')
    
    qr_code = restaurant.qr_codes.first()
    
    stats = {
        'categories_count': restaurant.categories.filter(is_active=True).count(),
        'items_count': MenuItem.objects.filter(category__restaurant=restaurant).count(),
        'items_available': MenuItem.objects.filter(category__restaurant=restaurant, is_available=True).count(),
    }
    
    context = {
        'restaurant': restaurant,
        'qr_code': qr_code,
        'stats': stats,
    }
    return render(request, 'restaurants/dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('restaurants:login')
