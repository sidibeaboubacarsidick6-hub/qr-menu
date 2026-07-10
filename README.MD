cat > README.md << 'EOF'
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
- **Frontend** : Tailwind CSS + JavaScript vanilla
- **QR Codes** : qrcode + Pillow

## 📦 Installation

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

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs (DB_NAME, DB_PASSWORD, SECRET_KEY...)

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