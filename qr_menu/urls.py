from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda r: redirect('restaurants:dashboard')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('apps.restaurants.urls')),
    path('', include('apps.menus.urls')),
    path('', include('apps.qrcodes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
