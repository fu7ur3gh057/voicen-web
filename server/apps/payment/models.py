from django.db import models, transaction
import uuid
import django
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django_celery_beat.models import PeriodicTask
from django_enum_choices.fields import EnumChoiceField
from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile
from constants import voicen_constants
from constants.interval_enums import TaskStatus, TimeInterval, interval_schedule
from django.utils.translation import gettext_lazy as _
import datetime

User = get_user_model()


class Wallet(TimeStampedUUIDModel):
    profile = models.OneToOneField(Profile, related_name='wallet', on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=15, decimal_places=5)

    @property
    def email(self):
        return self.profile.user_email

    @property
    def username(self):
        return self.profile.user.username

    def __str__(self):
        return f"{self.profile.user_email}"


class Subscription(TimeStampedUUIDModel):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Expired'),
        (3, 'Canceled'),
        (4, 'None')
    )
    wallet = models.ForeignKey(Wallet, related_name="subscription_list", on_delete=models.CASCADE)
    type = models.IntegerField(choices=STATUS_CHOICES, default=4)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save()
        save_date = self.created_at
        year = save_date.year
        month = save_date.month + 1
        day = save_date.day
        if month > 12:
            month = 1
            year += 1
        self.end_time = datetime.datetime(year, month, day)
        super().save()

    def __str__(self):
        return f"{self.wallet} subscription"


# Transaction For Updating Balance
class Transaction(TimeStampedUUIDModel):
    TRANSACTION_CHOICES = (
        (1, 'Pay As You Go'),
        (2, 'Subscription')
    )
    wallet = models.ForeignKey(Wallet, related_name="transaction_list", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.IntegerField(choices=TRANSACTION_CHOICES, default=1)

    def __str__(self):
        return f"{self.wallet} transaction"


class EPointLogs(models.Model):
    wallet = models.ForeignKey(Wallet, related_name="epoint_logs", on_delete=models.CASCADE)
    request_body = models.TextField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "EPoint Log"
        verbose_name_plural = "EPoint Logs"

    def __str__(self):
        return f'{self.id} | {self.wallet}'


class Operation(TimeStampedUUIDModel):
    OPERATION_CHOICES = (
        (1, 'Pay As You Go'),
        (2, 'Subscription'),
        (3, 'Synthesis'),
        (4, 'Transcribe'),
        (5, 'Transaction'),
    )
    wallet = models.ForeignKey(Wallet, related_name="operation_list", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.1)
    type = models.IntegerField(choices=OPERATION_CHOICES, default=1)

    def __str__(self):
        return f"{self.wallet} operation"


class SubscriptionChecker(models.Model):
    title = models.CharField(max_length=70, blank=False)
    task = models.OneToOneField(PeriodicTask, related_name='subscription_checker', on_delete=models.CASCADE, null=True,
                                blank=True, verbose_name=_("Subscription Checker Task"))
    time_interval = EnumChoiceField(TimeInterval, default=TimeInterval.one_day)
    status = EnumChoiceField(TaskStatus, default=TaskStatus.active)

    class Meta:
        verbose_name = "Subscription Checker"
        verbose_name_plural = "Subscription Checker"

    @transaction.atomic
    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=f'Subscription Checker Task',
            task='subscription_checker',
            interval=interval_schedule(self.time_interval),
            start_time=timezone.now()
        )

    def save(self, *args, **kwargs):
        count = SubscriptionChecker.objects.all().count()
        is_new = self.pk is None
        if not is_new:
            super().save()
        elif count > 0:
            return
        else:
            super().save()
        # if is_new:
        #     if count == 0:
        #         super().save()
        # elif count == 1 and not is_new:
        #     super().save()
        # else:
        #     return

    def delete(self, *args, **kwargs):
        task = self.task
        super().delete()
        task.delete()

    def __str__(self):
        return self.title
