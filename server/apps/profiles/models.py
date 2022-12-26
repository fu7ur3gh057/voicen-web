import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), max_length=30, default="+994507265559")
    profile_photo = models.ImageField(verbose_name=_("Profile Image"), default="/ui/profile_default.png")
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    postal_code = models.CharField(blank=True, null=True, max_length=100)
    api_token = models.UUIDField(blank=False, null=True, max_length=50, default=uuid.uuid4)
    # credit = models.DecimalField(max_digits=15, decimal_places=5, default=voicen_constants.START_CREDIT)
    is_subscribed = models.BooleanField(default=False)
    is_trial = models.BooleanField(default=True)

    @property
    def user_email(self):
        return self.user.email

    def __str__(self):
        return f"{self.user.email}"
