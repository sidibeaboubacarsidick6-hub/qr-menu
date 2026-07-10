# apps/qrcodes/urls.py

from django.urls import path
from . import views

app_name = 'qrcodes'

urlpatterns = [
    path('m/<uuid:uuid>/', views.public_menu, name='public_menu'),
    path('api/m/<uuid:uuid>/categories/', views.load_more_categories, name='load_categories'),
    path('api/m/<uuid:uuid>/categories/<int:category_id>/items/', views.load_category_items, name='load_items'),
]