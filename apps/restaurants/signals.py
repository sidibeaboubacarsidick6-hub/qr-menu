# apps/restaurants/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QRCode, Restaurant
from .utils import generate_qr_code


@receiver(post_save, sender=QRCode)
def create_qr_image(sender, instance, created, **kwargs):
    """Génère l'image du QR code automatiquement après création."""
    if created and not instance.qr_image:
        generate_qr_code(instance)
        instance.save()