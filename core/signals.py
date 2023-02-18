from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Picture, Account


@receiver(post_save, sender=Picture)
def resize(sender, instance, **kwargs):
    # TODO resize image, override
    print(instance.get_sizes())
