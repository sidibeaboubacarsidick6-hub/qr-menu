from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Restaurant(models.Model):
    """Un restaurant créé par le Super Admin."""
    
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='restaurant',
        verbose_name="Propriétaire"
    )
    name = models.CharField(max_length=200, verbose_name="Nom du restaurant")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    logo = models.ImageField(
        upload_to='restaurants/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Personnalisation
    primary_color = models.CharField(max_length=7, default='#1e40af', verbose_name="Couleur primaire")
    secondary_color = models.CharField(max_length=7, default='#f59e0b', verbose_name="Couleur secondaire")
    background_color = models.CharField(max_length=7, default='#f9fafb', verbose_name="Couleur de fond")
    text_color = models.CharField(max_length=7, default='#1f2937', verbose_name="Couleur du texte")
    header_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=1.00, verbose_name="Opacité du header")
    
    # Langue
    language = models.CharField(max_length=2, choices=[('fr', 'Français'), ('en', 'English')], default='fr', verbose_name="Langue du menu")
    
    # Abonnement
    subscription_end = models.DateField(null=True, blank=True, verbose_name="Abonnement jusqu'au")
    is_active = models.BooleanField(default=True, verbose_name="Menu actif")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class QRCode(models.Model):
    """Un QR code unique par restaurant."""
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='qr_codes',
        verbose_name="Restaurant"
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, verbose_name="Image QR Code")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "QR Code"
        verbose_name_plural = "QR Codes"

    def __str__(self):
        return f"QR {self.restaurant.name} - {self.uuid}"

    def get_menu_url(self):
        return f"/m/{self.uuid}/"
