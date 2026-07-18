# apps/restaurants/urls.py

from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('apparence/', views.customize_appearance, name='customize_appearance'),
    path('logout/', views.logout_view, name='logout'),
]