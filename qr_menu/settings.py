import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Sécurité
# ==========================

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Refuse de démarrer en production avec la clé de développement par défaut.
if not DEBUG and SECRET_KEY == 'dev-secret-change-me':
    raise RuntimeError(
        "SECRET_KEY par défaut détectée avec DEBUG=False. "
        "Définissez une vraie valeur pour SECRET_KEY dans votre fichier .env avant de déployer."
    )

# URL publique du site (utilisée notamment pour générer les QR codes).
# En production, définissez SITE_URL=https://votre-domaine.tld dans le .env
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000').rstrip('/')

# Origines de confiance pour le CSRF (nécessaire derrière un reverse proxy HTTPS).
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()
]

# Durcissement de sécurité activé automatiquement hors mode DEBUG.
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '3600'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = 'DENY'

# ==========================
# Internationalisation
# ==========================

LANGUAGE_CODE = 'fr'

LANGUAGES = [
    ('fr', _('Français')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

# ==========================
# Applications installées
# ==========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications du projet
    'apps.restaurants',
    'apps.menus',
    'apps.qrcodes',
]

# ==========================
# Middleware
# ==========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Gestion automatique de la langue
    'django.middleware.locale.LocaleMiddleware',

    # Middlewares personnalisés
    'apps.qrcodes.middleware.RestaurantLanguageMiddleware',
    'apps.restaurants.middleware.RedirectAuthenticatedRestaurantMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'qr_menu.urls'

# ==========================
# Templates
# ==========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qr_menu.wsgi.application'

# ==========================
# Base de données
# ==========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'qrmenu'),
        'USER': os.getenv('DB_USER', 'qrmenu_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ==========================
# Validation des mots de passe
# ==========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================
# Fichiers statiques
# ==========================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==========================
# Fichiers médias
# ==========================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# Clé primaire par défaut
# ==========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================
# Authentification
# ==========================

LOGIN_URL = 'restaurants:login'
LOGIN_REDIRECT_URL = 'restaurants:dashboard'
LOGOUT_REDIRECT_URL = 'restaurants:login'

# ==========================
# Logging
# ==========================

# On s'assure que le dossier existe : ce dossier n'est pas versionné dans Git
# (les .log sont ignorés), donc il doit être recréé après un clone frais,
# sinon Django plante au démarrage (FileHandler ne crée pas les dossiers).
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'errors.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
