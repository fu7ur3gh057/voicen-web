import logging

from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.chat.models import Room
from server.settings import AUTH_USER_MODEL

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_room(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            admins = User.objects.all().filter(Q(is_superuser=True) & Q(is_staff=True))
            room = Room.objects.create(user=instance)
            room.save()
            for superuser in admins:
                room.members.add(superuser)
            room.save()
            logger.info(f'{instance} room created')
