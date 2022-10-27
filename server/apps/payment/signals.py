import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payment.models import Operation, Transaction, Subscription, Wallet
from apps.profiles.models import Profile
from apps.synthesis.models import Synthesis
from apps.synthesis.utils import remove_text_inside_brackets, get_synthesis_price
from apps.transcribe.models import Transcribe
from apps.transcribe.utils import get_transcribe_price

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        wallet = Wallet.objects.create(profile=instance)
        wallet.save()


@receiver(post_save, sender=Wallet)
def create_init_subscription(sender, instance, created, **kwargs):
    if created:
        subscription = Subscription.objects.create(wallet=instance, type=4)
        subscription.save()


@receiver(post_save, sender=Synthesis)
def create_tts_operation(sender, instance, created, **kwargs):
    if created:
        char_size = remove_text_inside_brackets(instance.text)
        amount = get_synthesis_price(char_size=char_size)
        operation = Operation.objects.create(user=instance.user, amount=amount, type=3)
        operation.save()


@receiver(post_save, sender=Transcribe)
def create_transcribe_operation(sender, instance, created, **kwargs):
    if created:
        duration = instance.duration
        amount = get_transcribe_price(duration=duration)
        operation = Operation.objects.create(user=instance.user, amount=amount, type=4)
        operation.save()


@receiver(post_save, sender=Transaction)
def create_transaction_operation(sender, instance, created, **kwargs):
    if created:
        operation = Operation.objects.create(wallet=instance.wallet, amount=instance.amount, type=instance.type)
        operation.save()


@receiver(post_save, sender=Subscription)
def create_subscription_operation(sender, instance, created, **kwargs):
    if created and instance.type != 4:
        operation = Operation.objects.create(wallet=instance.wallet, amount=15, type=2)
        operation.save()
