import os

# 1. Charger .env AVANT tout
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, _, value = line.partition('=')
            os.environ[key.strip()] = value.strip()

# 2. Les tests ne doivent JAMAIS dépendre d'un service externe réel
# (Cloudflare R2, etc.) : plus lent, nécessite Internet, et peut échouer
# pour des raisons indépendantes du code testé (comme on vient de le voir).
# On force donc le stockage fichiers local le temps des tests, même si
# R2_ACCOUNT_ID est présent dans le .env pour le serveur de dev normal.
os.environ.pop('R2_ACCOUNT_ID', None)

# 3. Puis seulement maintenant, définir le settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'qr_menu.settings'

# 4. Maintenant on peut importer Django
import django
django.setup()
