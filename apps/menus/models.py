# apps/menus/models.py

from django.db import models
from apps.restaurants.models import Restaurant


class Category(models.Model):
    """Catégorie du menu : Entrées, Plats, Desserts..."""
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Restaurant"
    )
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']
        unique_together = ['restaurant', 'name']  # Pas 2x la même catégorie

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class MenuItem(models.Model):
    """Un plat ou boisson dans le menu."""
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Catégorie"
    )
    name = models.CharField(max_length=200, verbose_name="Nom du plat")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Prix (FCFA)"
    )
    image = models.ImageField(
        upload_to='menus/items/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Disponible"
    )
    is_vegetarian = models.BooleanField(
        default=False,
        verbose_name="Végétarien"
    )
    is_vegan = models.BooleanField(
        default=False,
        verbose_name="Végan"
    )
    is_gluten_free = models.BooleanField(
        default=False,
        verbose_name="Sans gluten"
    )
    allergens = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Allergènes",
        help_text="Séparés par des virgules : gluten, lactose, fruits à coque..."
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plat"
        verbose_name_plural = "Plats"
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.name} - {self.price} FCFA"