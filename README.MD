# 🍽️ QR Menu

Plateforme de menus digitaux pour restaurants. Remplacez les menus papier par un QR code élégant.

## ✨ Fonctionnalités

- 📱 Menu digital accessible via QR code
- 👨‍🍳 Dashboard restaurateur pour gérer son menu
- 🎨 Personnalisation des couleurs par restaurant
- 🌐 Multilingue (Français / Anglais)
- 🎠 Page publique animée avec carrousel de plats
- 💰 Gestion des abonnements avec désactivation automatique
- 📊 Super Admin pour gérer tous les restaurants

## 🛠️ Stack technique

- **Backend** : Django 5+
- **Base de données** : PostgreSQL
- **Frontend** : Tailwind CSS (CDN) + JavaScript vanilla
- **QR Codes** : qrcode + Pillow
- **Fichiers statiques** : WhiteNoise (servis directement par l'app, sans serveur web séparé)

## 📦 Installation (développement local)

### Prérequis

- Python 3.10+
- PostgreSQL

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/sidibeaboubacarsidick6-hub/qr-menu.git
cd qr-menu

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# 3. Installer les dépendances (requirements-dev.txt inclut aussi les outils de test)
pip install -r requirements-dev.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs (DB_NAME, DB_PASSWORD, SECRET_KEY, SITE_URL...)

# 5. Créer la base de données PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE qrmenu;"
sudo -u postgres psql -c "CREATE USER qrmenu_user WITH PASSWORD 'votre_mdp';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE qrmenu TO qrmenu_user;"
sudo -u postgres psql -c "ALTER DATABASE qrmenu OWNER TO qrmenu_user;"

# 6. Migrations
python manage.py migrate

# 7. Créer le Super Admin
python manage.py createsuperuser

# 8. Lancer le serveur
python manage.py runserver
```

Ensuite, connectez-vous sur `/admin/` avec le compte Super Admin pour créer un restaurant
(un utilisateur + un `Restaurant` associé). Le QR code est généré automatiquement à la création.

## 🚀 Déploiement en production

Points essentiels à ne pas oublier avant un déploiement :

- `DEBUG=False` et `SECRET_KEY` défini avec une vraie valeur aléatoire (l'application refuse de démarrer sinon).
- `ALLOWED_HOSTS` avec votre nom de domaine.
- **`SITE_URL`** avec l'URL publique réelle (ex. `https://menu.mon-domaine.com`) : c'est cette URL qui est encodée dans les QR codes générés. Sans cela, les QR codes pointeront vers `localhost`.
- `CSRF_TRUSTED_ORIGINS` si vous êtes derrière un proxy HTTPS (Nginx, Render, Railway...).
- Un serveur PostgreSQL accessible (les identifiants `DB_*`).
- Les fichiers statiques sont servis par WhiteNoise ; pensez à lancer `python manage.py collectstatic` au déploiement.
- **Stockage des médias** : les images (logos, photos de plats, QR codes) sont actuellement stockées sur le disque local (`MEDIA_ROOT`). Sur une plateforme à système de fichiers éphémère (Heroku, Render sans disque persistant...), ces fichiers seront perdus à chaque redéploiement. Pour de la production sérieuse, prévoyez un stockage externe (S3 compatible, via `django-storages`).

Un `Procfile` est fourni pour les plateformes de type Heroku/Render :

```
web: gunicorn qr_menu.wsgi --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
pytest
```

La CI (`.github/workflows/ci.yml`) exécute les tests contre une base PostgreSQL de test à chaque push/PR.

## 🗓️ Gestion des abonnements

La commande `python manage.py check_subscriptions` désactive automatiquement les restaurants dont
l'abonnement est expiré, et avertit ceux qui expirent dans 3 jours. À exécuter quotidiennement via
un cron / scheduler (ex. cron job de la plateforme d'hébergement).
