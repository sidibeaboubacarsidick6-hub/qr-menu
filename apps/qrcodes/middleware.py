# apps/qrcodes/middleware.py

from django.utils import translation
from apps.restaurants.models import QRCode


class RestaurantLanguageMiddleware:
    """
    Détecte la langue du restaurant depuis l'URL du QR code
    et active la langue correspondante.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si on est sur une page de menu public
        path = request.path
        if path.startswith('/m/') and '/m/' in path:
            try:
                # Extraire l'UUID de l'URL
                uuid = path.split('/m/')[1].split('/')[0]
                qr = QRCode.objects.filter(uuid=uuid).first()
                if qr and qr.restaurant.language:
                    translation.activate(qr.restaurant.language)
                    request.LANGUAGE_CODE = qr.restaurant.language
            except (ValueError, IndexError):
                pass
        
        response = self.get_response(request)
        return response