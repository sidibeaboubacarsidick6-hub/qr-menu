# apps/qrcodes/middleware.py

from django.conf import settings
from django.utils import translation
from apps.restaurants.models import QRCode

# Clé de session utilisée pour mémoriser le choix explicite de langue du
# visiteur sur la page publique du menu (sélecteur FR/EN). On utilise une clé
# propre au projet plutôt qu'une constante Django : LANGUAGE_SESSION_KEY,
# présente dans d'anciennes versions de Django, n'existe plus depuis que le
# framework est passé à un cookie dédié pour la langue "globale" du site.
LANGUAGE_SESSION_KEY = 'qr_menu_language'


class RestaurantLanguageMiddleware:
    """
    Active la langue à utiliser sur la page publique du menu (et ses
    endpoints API associés).

    Ordre de priorité :
    1. Paramètre `?lang=fr` ou `?lang=en` dans l'URL (choix explicite du
       client sur le sélecteur FR/EN affiché sur la page du menu). Ce choix
       est mémorisé en session pour rester actif sur les pages suivantes
       (y compris les appels AJAX de "charger plus").
    2. Langue déjà choisie précédemment en session pour ce visiteur.
    3. Langue par défaut configurée par le restaurateur (Restaurant.language).

    NB : avant ce correctif, le sélecteur FR/EN affiché sur le menu public
    ne faisait strictement rien : aucun code ne lisait le paramètre `?lang=`.
    """

    MENU_PATH_PREFIXES = ('/m/', '/api/m/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith(self.MENU_PATH_PREFIXES):
            language = None

            requested_lang = request.GET.get('lang')
            valid_codes = {code for code, _ in settings.LANGUAGES}
            if requested_lang in valid_codes:
                language = requested_lang
                request.session[LANGUAGE_SESSION_KEY] = language
            elif LANGUAGE_SESSION_KEY in request.session:
                language = request.session[LANGUAGE_SESSION_KEY]

            if language is None:
                try:
                    prefix = '/m/' if path.startswith('/m/') else '/api/m/'
                    uuid = path.split(prefix, 1)[1].split('/')[0]
                    qr = QRCode.objects.select_related('restaurant').filter(uuid=uuid).first()
                    if qr and qr.restaurant.language:
                        language = qr.restaurant.language
                except (ValueError, IndexError):
                    language = None

            if language:
                translation.activate(language)
                request.LANGUAGE_CODE = language

        response = self.get_response(request)
        return response
