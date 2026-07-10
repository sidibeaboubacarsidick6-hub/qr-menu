# apps/restaurants/apps.py

from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.restaurants'  # Chemin complet !
    verbose_name = "Restaurants"

    def ready(self):
        import apps.restaurants.signals