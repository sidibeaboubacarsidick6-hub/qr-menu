# apps/menus/urls.py

from django.urls import path
from . import views

app_name = 'menus'

urlpatterns = [
    # Catégories
    path('categories/', views.category_list, name='category_list'),
    path('categories/ajouter/', views.category_create, name='category_create'),
    path('categories/<int:pk>/modifier/', views.category_update, name='category_update'),
    path('categories/<int:pk>/supprimer/', views.category_delete, name='category_delete'),
    
    # Plats
    path('plats/', views.item_list, name='item_list'),
    path('plats/ajouter/', views.item_create, name='item_create'),
    path('plats/<int:pk>/modifier/', views.item_update, name='item_update'),
    path('plats/<int:pk>/supprimer/', views.item_delete, name='item_delete'),
]