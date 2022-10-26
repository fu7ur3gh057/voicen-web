from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile
from apps.transcribe.utils import transcribe_file_path
from django.utils.translation import gettext_lazy as _


class Transcribe(TimeStampedUUIDModel):
    LANGUAGE_CHOICES = (
        (None, 'Choose language'),
        ('en', 'English'),
        ('az', 'Azərbaycan'),
        ('tr', 'Türkçe'),
        ('ru', 'Русский'),
    )
    profile = models.ForeignKey(Profile, related_name="transcribe_jobs", on_delete=models.CASCADE)
    lang = models.CharField(verbose_name=_("Language"), max_length=3, blank=False, choices=LANGUAGE_CHOICES)
    result_path = models.CharField(verbose_name=_("Result Path"), max_length=256, null=True)
    youtube_url = models.CharField(verbose_name=_("Youtube Url"), max_length=256, null=True)
    file = models.FileField(max_length=300, upload_to=transcribe_file_path, null=True)
    file_name = models.CharField(verbose_name=_("File Name"), max_length=256, null=True)
    duration = models.DecimalField(max_digits=6, decimal_places=3, default=0.00)
    full_text = models.TextField(verbose_name=_("Full Text"), default='')
    edited_json = models.JSONField(null=True)
    # result_json = jsonfield.JSONField(verbose_name=_("Result JSON"), null=True)
    status = models.IntegerField(default=0)
    progress = models.DecimalField(max_digits=15, decimal_places=6, default=0.00)
    error_code = models.IntegerField(verbose_name=_("Error Code"), default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Transcribe"
        verbose_name_plural = "Transcribe Jobs"

    def email(self):
        return self.profile.user_email

    def __str__(self):
        return str(self.id)
