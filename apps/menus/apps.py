# apps/menus/apps.py

from django.apps import AppConfig


class MenusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.menus'  # Chemin complet !
    verbose_name = "Menus"