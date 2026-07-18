"""
Commande de diagnostic temporaire pour Cloudflare R2.

Objectif : afficher le détail COMPLET de l'erreur retournée par R2 (code
d'erreur exact, message, request-id...), que Django masque habituellement
derrière un message générique ("400 Bad Request"). À exécuter une seule fois
via le Build Command de Render (pas d'accès Shell sur le plan gratuit), en
lisant le résultat dans les logs de build.

À SUPPRIMER une fois le diagnostic terminé : cette commande imprime des
informations de configuration (nom du bucket, endpoint, identifiants
partiellement masqués) dans les logs, ce qui ne doit pas rester en place
indéfiniment sur un projet en production.
"""
import boto3
from botocore.config import Config
from django.conf import settings
from django.core.management.base import BaseCommand


def mask(value, keep=4):
    if not value:
        return "(vide)"
    return value[:keep] + "…" + f"({len(value)} caractères)"


class Command(BaseCommand):
    help = "Diagnostic Cloudflare R2 : affiche le détail complet d'une éventuelle erreur de connexion."

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("DIAGNOSTIC CLOUDFLARE R2")
        self.stdout.write("=" * 70)

        use_r2 = getattr(settings, "USE_R2", False)
        self.stdout.write(f"USE_R2 détecté par settings.py : {use_r2}")

        if not use_r2:
            self.stdout.write(self.style.ERROR(
                "USE_R2 est False : la variable R2_ACCOUNT_ID n'est probablement "
                "pas définie (ou vide) sur cet environnement. Rien d'autre à "
                "diagnostiquer tant que ce n'est pas corrigé."
            ))
            return

        account_id = settings.R2_ACCOUNT_ID if hasattr(settings, "R2_ACCOUNT_ID") else None
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
        access_key = getattr(settings, "AWS_ACCESS_KEY_ID", None)
        secret_key = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)
        endpoint = getattr(settings, "AWS_S3_ENDPOINT_URL", None)
        custom_domain = getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)

        self.stdout.write(f"R2_ACCOUNT_ID    : {mask(account_id)}")
        self.stdout.write(f"Bucket           : {bucket!r}")
        self.stdout.write(f"Access Key ID    : {mask(access_key)}")
        self.stdout.write(f"Secret Access Key: {mask(secret_key)}")
        self.stdout.write(f"Endpoint URL     : {endpoint!r}")
        self.stdout.write(f"Custom domain    : {custom_domain!r}")
        self.stdout.write("-" * 70)

        client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="auto",
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        )

        # Test 1 : head_bucket (le test le plus simple possible -- juste
        # vérifier que le bucket existe et que les identifiants sont valides,
        # sans toucher à un objet particulier).
        self.stdout.write("Test 1 : head_bucket...")
        try:
            resp = client.head_bucket(Bucket=bucket)
            self.stdout.write(self.style.SUCCESS(f"  OK : {resp['ResponseMetadata']['HTTPStatusCode']}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ECHEC : {repr(e)}"))
            response = getattr(e, "response", None)
            if response:
                self.stdout.write(f"  Détail complet de la réponse R2 : {response}")

        # Test 2 : list_objects_v2 (confirme les droits de lecture sur le bucket)
        self.stdout.write("Test 2 : list_objects_v2...")
        try:
            resp = client.list_objects_v2(Bucket=bucket, MaxKeys=1)
            self.stdout.write(self.style.SUCCESS(f"  OK : {resp['ResponseMetadata']['HTTPStatusCode']}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ECHEC : {repr(e)}"))
            response = getattr(e, "response", None)
            if response:
                self.stdout.write(f"  Détail complet de la réponse R2 : {response}")

        # Test 3 : head_object sur une clé qui n'existe presque certainement
        # pas -- c'est EXACTEMENT l'appel qui plante dans l'application réelle.
        self.stdout.write("Test 3 : head_object sur une clé inexistante...")
        try:
            resp = client.head_object(Bucket=bucket, Key="diagnostic-inexistant.png")
            self.stdout.write(self.style.SUCCESS(f"  OK (inattendu, le fichier existe ?) : {resp}"))
        except client.exceptions.ClientError as e:
            code = e.response.get("Error", {}).get("Code")
            if code == "404" or code == "NoSuchKey":
                self.stdout.write(self.style.SUCCESS(
                    "  OK : 404/NoSuchKey reçu normalement (le fichier n'existe pas, "
                    "c'est le comportement attendu -- la connexion à R2 fonctionne !)"
                ))
            else:
                self.stdout.write(self.style.ERROR(f"  ECHEC inattendu : {repr(e)}"))
                self.stdout.write(f"  Détail complet de la réponse R2 : {e.response}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ECHEC : {repr(e)}"))
            response = getattr(e, "response", None)
            if response:
                self.stdout.write(f"  Détail complet de la réponse R2 : {response}")

        self.stdout.write("=" * 70)
        self.stdout.write("FIN DU DIAGNOSTIC")
        self.stdout.write("=" * 70)
