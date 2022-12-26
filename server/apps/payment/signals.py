import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.models import VoicenConfiguration
from apps.payment.models import Operation, Transaction, Subscription, Wallet, SubscriptionChecker
from apps.profiles.models import Profile
from apps.synthesis.models import Synthesis
from apps.transcribe.models import Transcribe
from constants.interval_enums import TaskStatus, interval_schedule

logger = logging.getLogger(__name__)


# CREATE WALLET AFTER PROFILE CREATING
@receiver(post_save, sender=Profile)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        config = VoicenConfiguration.objects.all().first()
        wallet = Wallet.objects.create(profile=instance, credit=config.trial_credit)
        wallet.save()


# CREATE INIT SUBSCRIPTION WITH TYPE NONE
@receiver(post_save, sender=Wallet)
def create_init_subscription(sender, instance, created, **kwargs):
    if created:
        subscription = Subscription.objects.create(wallet=instance, type=4)
        subscription.save()


# CREATE OPERATION TYPE - SYNTHESIS
@receiver(post_save, sender=Synthesis)
def create_synthesis_operation(sender, instance, created, **kwargs):
    if created:
        amount = instance.price
        operation = Operation.objects.create(wallet=instance.profile.wallet, amount=amount, type=3)
        operation.save()


# CREATE OPERATION TYPE - TRANSCRIBE
@receiver(post_save, sender=Transcribe)
def create_transcribe_operation(sender, instance, created, **kwargs):
    if created:
        amount = instance.price
        operation = Operation.objects.create(wallet=instance.profile.wallet, amount=amount, type=4)
        operation.save()


# CREATE OPERATION TYPE - TRANSACTION
@receiver(post_save, sender=Transaction)
def create_transaction_operation(sender, instance, created, **kwargs):
    if created:
        operation = Operation.objects.create(wallet=instance.wallet, amount=instance.amount, type=instance.type)
        operation.save()


# CREATE OPERATION TYPE - SUBSCRIPTION
@receiver(post_save, sender=Subscription)
def create_subscription_operation(sender, instance, created, **kwargs):
    if created and instance.type != 4:
        operation = Operation.objects.create(wallet=instance.wallet, amount=15, type=2)
        operation.save()


# CREATE SUBSCRIPTION CHECKER TASK
@receiver(post_save, sender=SubscriptionChecker)
def create_or_update_checker(sender, instance, created, **kwargs):
    if created:
        try:
            count = SubscriptionChecker.objects.all().count()
            if count <= 1:
                instance.setup_task()
        except Exception as ex:
            print(ex)
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.interval = interval_schedule(instance.time_interval)
            instance.task.save()

# @receiver(pre_delete, sender=SubscriptionChecker)
# def pre_delete_checker(sender, instance, **kwargs):
#     instance.task.delete()
