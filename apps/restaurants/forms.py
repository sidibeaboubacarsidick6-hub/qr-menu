# apps/restaurants/forms.py

from django import forms
from .models import Restaurant


class RestaurantAppearanceForm(forms.ModelForm):
    """
    Formulaire de personnalisation de l'apparence du menu public, pensé pour
    un restaurateur sans vocabulaire technique : pas de "code hexadécimal",
    juste des pastilles de couleur à cliquer et un curseur pour l'ambiance
    de la photo de couverture.
    """
    class Meta:
        model = Restaurant
        fields = ['primary_color', 'secondary_color', 'background_color', 'text_color', 'header_opacity']
        labels = {
            'primary_color': "Couleur principale",
            'secondary_color': "Couleur d'accent",
            'background_color': "Couleur de fond",
            'text_color': "Couleur du texte",
            'header_opacity': "Ambiance de la photo de couverture",
        }
        help_texts = {
            'primary_color': "Utilisée pour les boutons et les titres importants.",
            'secondary_color': "Utilisée pour les petits détails et icônes.",
            'background_color': "La couleur de fond derrière votre menu.",
            'text_color': "La couleur du texte affiché à vos clients.",
            'header_opacity': "Plus la valeur est haute, plus la photo d'en-tête est assombrie (pour que le texte reste lisible par-dessus).",
        }
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'header_opacity': forms.NumberInput(attrs={
                'type': 'range', 'min': '0', 'max': '1', 'step': '0.05',
            }),
        }
