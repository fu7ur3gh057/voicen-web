import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from server.settings import AUTH_USER_MODEL
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


# CREATE PROFILE AFTER USER CREATING
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_us_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# CREATE PROFILE AFTER USER CREATING
@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f'{instance} profile created')
