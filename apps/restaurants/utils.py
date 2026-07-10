# apps/restaurants/utils.py

import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


def generate_qr_code(qr_instance, base_url="http://localhost:8000"):
    """
    Génère une image QR code PNG pour une instance QRCode.
    L'URL encodée pointe vers la page publique du menu.
    """
    menu_url = f"{base_url}/m/{qr_instance.uuid}/"
    
    # Création du QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)
    
    # Génération de l'image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Sauvegarde dans un buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    filename = f"qr_{qr_instance.restaurant.slug}_{qr_instance.uuid}.png"
    
    # Sauvegarde dans le champ ImageField
    qr_instance.qr_image.save(
        filename,
        ContentFile(buffer.getvalue()),
        save=False
    )