from django.contrib.auth import get_user_model
from django.db import models

from apps.profiles.models import Profile
from constants import voicen_constants
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Synthesis(TimeStampedUUIDModel):
    LANGUAGE_CHOICES = (
        (None, _('Choose language')),
        ('az', 'Azərbaycan'),
        ('tr', 'Türkçe'),
        ('ru', 'Русский'),
    )

    profile = models.ForeignKey(Profile, related_name="synthesis_jobs", on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=256, blank=True, null=True)
    result_path = models.CharField(max_length=256, null=True)
    voice = models.IntegerField(choices=voicen_constants.VOICE_CHOICES)
    num_characters = models.BigIntegerField(blank=True, null=True)
    lang = models.CharField(verbose_name=_("Language"), max_length=3, blank=False, choices=LANGUAGE_CHOICES)
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Synthesis"
        verbose_name_plural = "Synthesis Jobs"

    def email(self):
        return self.profile.user_email

    def __str__(self):
        return str(self.id)
