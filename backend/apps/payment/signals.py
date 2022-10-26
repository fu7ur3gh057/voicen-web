import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payment.models import Operation, Transaction, Subscription, Wallet
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        wallet = Wallet.objects.create(profile=instance)
        wallet.save()
