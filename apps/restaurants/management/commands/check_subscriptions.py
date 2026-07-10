from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from apps.restaurants.models import Restaurant


class Command(BaseCommand):
    help = 'Désactive les restaurants dont l\'abonnement a expiré'

    def handle(self, *args, **kwargs):
        today = date.today()
        
        # Restaurants expirés mais encore actifs
        expired = Restaurant.objects.filter(
            subscription_end__lt=today,
            is_active=True
        )
        
        count = expired.count()
        
        for resto in expired:
            resto.is_active = False
            resto.save()
            self.stdout.write(
                self.style.WARNING(
                    f"❌ Désactivé : {resto.name} (expiré le {resto.subscription_end})"
                )
            )
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS("✅ Aucun abonnement expiré aujourd'hui."))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"\n✅ {count} restaurant(s) désactivé(s).")
            )
        
        # Avertir les restaurants qui expirent dans 3 jours
        warning_date = today + timezone.timedelta(days=3)
        soon_expired = Restaurant.objects.filter(
            subscription_end=warning_date,
            is_active=True
        )
        
        for resto in soon_expired:
            self.stdout.write(
                self.style.NOTICE(
                    f"⚠️ Expire bientôt : {resto.name} (le {resto.subscription_end})"
                )
            )
