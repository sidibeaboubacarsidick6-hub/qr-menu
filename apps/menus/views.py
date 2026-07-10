# apps/menus/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.restaurants.models import Restaurant
from .models import Category, MenuItem
from .forms import CategoryForm, MenuItemForm


@login_required
def category_list(request):
    """Liste des catégories du restaurant."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    categories = restaurant.categories.all().order_by('order', 'name')
    
    context = {
        'restaurant': restaurant,
        'categories': categories,
    }
    return render(request, 'menus/category_list.html', context)


@login_required
def category_create(request):
    """Créer une nouvelle catégorie."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.restaurant = restaurant
            category.save()
            messages.success(request, f"Catégorie '{category.name}' créée !")
            return redirect('menus:category_list')
    else:
        form = CategoryForm()
    
    context = {
        'restaurant': restaurant,
        'form': form,
        'action': 'Créer',
    }
    return render(request, 'menus/category_form.html', context)


@login_required
def category_update(request, pk):
    """Modifier une catégorie."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    category = get_object_or_404(Category, pk=pk, restaurant=restaurant)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Catégorie '{category.name}' mise à jour !")
            return redirect('menus:category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'restaurant': restaurant,
        'form': form,
        'action': 'Modifier',
        'category': category,
    }
    return render(request, 'menus/category_form.html', context)


@login_required
def category_delete(request, pk):
    """Supprimer une catégorie."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    category = get_object_or_404(Category, pk=pk, restaurant=restaurant)
    
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Catégorie '{name}' supprimée !")
        return redirect('menus:category_list')
    
    context = {
        'restaurant': restaurant,
        'category': category,
    }
    return render(request, 'menus/category_confirm_delete.html', context)

@login_required
def item_list(request):
    """Liste des plats du restaurant."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    items = MenuItem.objects.filter(category__restaurant=restaurant).select_related('category')
    items = items.order_by('category__order', 'category__name', 'order', 'name')
    
    context = {
        'restaurant': restaurant,
        'items': items,
    }
    return render(request, 'menus/item_list.html', context)


@login_required
def item_create(request):
    """Ajouter un nouveau plat."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, restaurant=restaurant)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Plat '{item.name}' ajouté !")
            return redirect('menus:item_list')
    else:
        form = MenuItemForm(restaurant=restaurant)
    
    context = {
        'restaurant': restaurant,
        'form': form,
        'action': 'Ajouter',
    }
    return render(request, 'menus/item_form.html', context)


@login_required
def item_update(request, pk):
    """Modifier un plat."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    item = get_object_or_404(MenuItem, pk=pk, category__restaurant=restaurant)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item, restaurant=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, f"Plat '{item.name}' mis à jour !")
            return redirect('menus:item_list')
    else:
        form = MenuItemForm(instance=item, restaurant=restaurant)
    
    context = {
        'restaurant': restaurant,
        'form': form,
        'action': 'Modifier',
        'item': item,
    }
    return render(request, 'menus/item_form.html', context)


@login_required
def item_delete(request, pk):
    """Supprimer un plat."""
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    item = get_object_or_404(MenuItem, pk=pk, category__restaurant=restaurant)
    
    if request.method == 'POST':
        name = item.name
        item.delete()
        messages.success(request, f"Plat '{name}' supprimé !")
        return redirect('menus:item_list')
    
    context = {
        'restaurant': restaurant,
        'item': item,
    }
    return render(request, 'menus/item_confirm_delete.html', context)