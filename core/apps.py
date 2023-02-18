from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_base_tiers(**kwargs):
    from core.models import Tier
    try:
        Tier.objects.all()
    except:
        pass


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(create_base_tiers, sender=self)
