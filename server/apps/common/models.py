import uuid
from django.utils.translation import gettext_lazy as _

from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class VoicenConfiguration(models.Model):
    minimum_price = models.DecimalField(verbose_name=_("Minimal Price"), decimal_places=2, default=1, max_digits=5)
    transcribe_price = models.DecimalField(verbose_name=_("Transcribe Price"),
                                           decimal_places=3,
                                           default=0.06,
                                           max_digits=5,
                                           help_text='For each second')
    synthesis_price = models.DecimalField(verbose_name=_("Synthesis Price"),
                                          decimal_places=3,
                                          default=0.05,
                                          max_digits=5,
                                          help_text='For each symbol')
    dollar_in_azn = models.DecimalField(verbose_name=_("One USD in AZN"),
                                        decimal_places=2,
                                        default=1.7,
                                        max_digits=5)
    trial_credit = models.DecimalField(max_digits=5, decimal_places=2, default=1.20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Voicen Configuration"
        verbose_name_plural = "Voicen Configuration"

    def save(self, *args, **kwargs):
        count = VoicenConfiguration.objects.all().count()
        is_new = self.pk is None
        if not is_new:
            super().save()
        elif count > 0:
            return
        else:
            super().save()

    def __str__(self):
        return 'Voicen Configuration'
