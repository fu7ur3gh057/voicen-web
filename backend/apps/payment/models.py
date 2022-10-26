from django.db import models
import uuid
import django
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile
from constants import voicen_constants

User = get_user_model()


class Wallet(TimeStampedUUIDModel):
    profile = models.OneToOneField(Profile, related_name='wallet', on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=15, decimal_places=5, default=voicen_constants.START_CREDIT)

    def email(self):
        return self.profile.user_email

    def __str__(self):
        return f"{self.profile.user_email}"


class Subscription(TimeStampedUUIDModel):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Expired'),
        (3, 'Canceled'),
    )
    wallet = models.ForeignKey(Wallet, related_name="subscription_list", on_delete=models.CASCADE)
    type = models.IntegerField(choices=STATUS_CHOICES, default=1)


# Transaction For Updating Balance
class Transaction(TimeStampedUUIDModel):
    TRANSACTION_CHOICES = (
        (1, 'Pay As You Go'),
        (2, 'Subscription')
    )
    wallet = models.ForeignKey(Wallet, related_name="transaction_list", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.IntegerField(choices=TRANSACTION_CHOICES, default=1)


class Operation(TimeStampedUUIDModel):
    OPERATION_CHOICES = (
        (1, 'Pay As You Go'),
        (2, 'Subscription'),
        (3, 'Text To Speech'),
        (4, 'Speech To Text'),
        (5, 'Transaction'),
    )
    wallet = models.ForeignKey(Wallet, related_name="operation_list", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.1)
    type = models.IntegerField(choices=OPERATION_CHOICES, default=1)
