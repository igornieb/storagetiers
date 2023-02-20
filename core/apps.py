from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_base_tiers(**kwargs):
    from core.models import Tier
    try:
        Tier.objects.create(name="Basic", sizes_allowed="200")
        Tier.objects.create(name="Premium", sizes_allowed="200, 400", allow_original=True)
        Tier.objects.create(name="Enterprise", sizes_allowed="200 400", allow_original=True, allow_link=True)
        print("Tiers created")
    except:
        print("Tiers already created")


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(create_base_tiers, sender=self)
        import core.signals
