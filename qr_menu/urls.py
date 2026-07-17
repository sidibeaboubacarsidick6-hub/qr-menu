from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as serve_static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda r: redirect('restaurants:dashboard')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('apps.restaurants.urls')),
    path('', include('apps.menus.urls')),
    path('', include('apps.qrcodes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Fichiers médias (photos de plats, logos, QR codes générés) : servis par
# Django lui-même, en développement ET en production.
#
# Note : Django's static() helper (utilisé ci-dessus pour STATIC_URL) refuse
# volontairement de générer la moindre route tant que DEBUG=False, quel que
# soit l'endroit où on l'appelle -- c'est une sécurité intégrée au framework,
# pas un bug. On appelle donc directement la vue django.views.static.serve
# pour contourner cette limitation.
#
# Ce n'est pas la solution la plus performante à grande échelle (un vrai
# stockage externe type S3/Cloudinary serait préférable), mais c'est
# nécessaire tant qu'aucun stockage externe n'est configuré : sans cette
# route, TOUTES les images (QR codes inclus) renvoient une erreur 404 en
# production, WhiteNoise ne servant que les fichiers statiques (CSS/JS),
# jamais les médias.
urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
        serve_static,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
