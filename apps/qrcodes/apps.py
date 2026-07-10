# apps/qrcodes/apps.py

from django.apps import AppConfig


class QrcodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.qrcodes'  # Chemin complet !
    verbose_name = "QR Codes"