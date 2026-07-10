import os

# 1. Charger .env AVANT tout
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, _, value = line.partition('=')
            os.environ[key.strip()] = value.strip()

# 2. Puis seulement maintenant, définir le settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'qr_menu.settings'

# 3. Maintenant on peut importer Django
import django
django.setup()
