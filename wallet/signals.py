from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from wallet.models import Wallet


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance) # Checks: Q: Do we need wallet for patients, Q: can user type change later
