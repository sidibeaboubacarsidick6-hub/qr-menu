import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import dj_database_url


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Sécurité
# ==========================

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Render fournit automatiquement le nom de domaine réel du service
# (ex: qr-menu-503o.onrender.com) via cette variable, sans configuration
# manuelle. On s'en sert comme valeur par défaut intelligente pour
# ALLOWED_HOSTS / SITE_URL / CSRF_TRUSTED_ORIGINS : ça évite d'avoir à
# recopier à la main l'URL exacte (source d'erreurs de copier-coller).
# Ces 3 variables restent surchageables manuellement si besoin (ex: nom de
# domaine personnalisé).
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')

_default_allowed_hosts = 'localhost,127.0.0.1'
if RENDER_EXTERNAL_HOSTNAME:
    _default_allowed_hosts += f',{RENDER_EXTERNAL_HOSTNAME}'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', _default_allowed_hosts).split(',') if h.strip()]

# Refuse de démarrer en production avec la clé de développement par défaut.
if not DEBUG and SECRET_KEY == 'dev-secret-change-me':
    raise RuntimeError(
        "SECRET_KEY par défaut détectée avec DEBUG=False. "
        "Définissez une vraie valeur pour SECRET_KEY dans votre fichier .env avant de déployer."
    )

# URL publique du site (utilisée notamment pour générer les QR codes).
# En production, définissez SITE_URL=https://votre-domaine.tld dans le .env
# (déduite automatiquement sur Render si non définie explicitement).
_default_site_url = f'https://{RENDER_EXTERNAL_HOSTNAME}' if RENDER_EXTERNAL_HOSTNAME else 'http://localhost:8000'
SITE_URL = os.getenv('SITE_URL', _default_site_url).rstrip('/')

# Origines de confiance pour le CSRF (nécessaire derrière un reverse proxy HTTPS).
_default_csrf_origins = f'https://{RENDER_EXTERNAL_HOSTNAME}' if RENDER_EXTERNAL_HOSTNAME else ''
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', _default_csrf_origins).split(',') if o.strip()
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

# Le Franc CFA (FCFA) ne se subdivise pas en centimes dans l'usage courant ;
# le séparateur de milliers (ex: "2 500 FCFA") améliore la lisibilité.
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '

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

    # Stockage fichiers médias sur Cloudflare R2 (compatible S3)
    'storages',

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

    # Middleware personnalisé (langue par restaurant)
    'apps.qrcodes.middleware.RestaurantLanguageMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Doit impérativement venir APRÈS AuthenticationMiddleware :
    # il utilise request.user, qui n'existe pas avant.
    'apps.restaurants.middleware.RedirectAuthenticatedRestaurantMiddleware',

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

# Deux modes pris en charge :
# - DATABASE_URL (Neon, Render, Railway... fournissent une seule URL de connexion,
#   ex: postgres://user:pass@host/dbname?sslmode=require) -> utilisé en priorité.
# - Variables séparées DB_NAME / DB_USER / DB_PASSWORD / DB_HOST / DB_PORT,
#   pratiques en développement local.
#
# Nettoyage défensif : un copier-coller depuis l'interface web d'un hébergeur
# ajoute parfois des guillemets ou des espaces invisibles en début/fin de valeur.
DATABASE_URL = (os.getenv('DATABASE_URL') or '').strip().strip('"').strip("'")

# Render définit automatiquement la variable RENDER=true sur tous les services
# qu'il héberge. On s'en sert pour détecter qu'on tourne sur Render et EXIGER
# une DATABASE_URL valide, plutôt que de se rabattre silencieusement sur
# "localhost" (qui n'existe pas sur Render et produit une erreur psycopg2
# cryptique au lieu d'un message clair).
IS_RENDER = os.getenv('RENDER') == 'true'

if IS_RENDER and not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL est manquante ou vide alors que l'application tourne sur Render. "
        "Va dans Render -> ton service -> Environment, et vérifie que la variable "
        "DATABASE_URL contient bien la connection string PostgreSQL complète "
        "(fournie par Neon), sans guillemets ni espace autour."
    )

if DATABASE_URL and not DATABASE_URL.startswith(('postgres://', 'postgresql://')):
    raise RuntimeError(
        f"DATABASE_URL ne ressemble pas à une URL PostgreSQL valide "
        f"(elle devrait commencer par 'postgresql://'). Valeur actuelle : "
        f"{DATABASE_URL[:15]}... Vérifie qu'aucun caractère n'a été perdu ou "
        f"ajouté lors du copier-coller dans Render."
    )

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=os.getenv('DB_SSL_REQUIRE', 'True') == 'True',
        )
    }
else:
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

# ==========================
# Fichiers médias (Cloudflare R2)
# ==========================

# USE_R2 est activé automatiquement dès que R2_ACCOUNT_ID est défini dans
# l'environnement (local via .env, ou sur Render via Environment).
# Sans ces variables, l'app retombe sur le stockage disque local classique
# (pratique en dev si tu ne veux pas configurer R2 tout de suite).
USE_R2 = bool(os.getenv('R2_ACCOUNT_ID'))

if USE_R2:
    # Bug connu : les versions récentes de boto3/botocore envoient par défaut
    # des en-têtes de vérification (checksums) sur les requêtes S3, que
    # Cloudflare R2 rejette avec une erreur 400 Bad Request -- typiquement
    # sur les appels HeadObject (utilisés notamment pour vérifier si un
    # fichier existe déjà, comme lors de la régénération d'un QR code portant
    # toujours le même nom).
    #
    # On désactive ce comportement via un objet botocore.config.Config
    # explicite (AWS_S3_CLIENT_CONFIG), plus fiable que les variables
    # d'environnement : django-storages construit sinon sa propre Config par
    # défaut et ignore silencieusement certains réglages définis autrement.
    from botocore.config import Config as _BotoConfig

    AWS_S3_CLIENT_CONFIG = _BotoConfig(
        signature_version='s3v4',
        s3={'addressing_style': 'auto'},
        request_checksum_calculation='when_required',
        response_checksum_validation='when_required',
    )

    R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
    AWS_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com'
    AWS_S3_CUSTOM_DOMAIN = (
        os.getenv('R2_PUBLIC_URL', '')
        .replace('https://', '')
        .replace('http://', '')
        .rstrip('/')
    )
    AWS_S3_REGION_NAME = 'auto'
    AWS_DEFAULT_ACL = None
    # NB : AWS_S3_SIGNATURE_VERSION n'est plus utilisé ici -- il est inclus
    # directement dans AWS_S3_CLIENT_CONFIG ci-dessus, qui remplace
    # entièrement la Config par défaut que django-storages aurait construite.
    AWS_QUERYSTRING_AUTH = False  # URLs publiques propres, sans token d'expiration
    AWS_S3_FILE_OVERWRITE = False  # évite d'écraser un fichier existant portant le même nom

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN]):
        raise RuntimeError(
            "USE_R2 est activé (R2_ACCOUNT_ID détecté) mais une ou plusieurs variables "
            "R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY / R2_BUCKET_NAME / R2_PUBLIC_URL "
            "sont manquantes. Vérifie ton .env ou les variables d'environnement sur Render."
        )
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

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