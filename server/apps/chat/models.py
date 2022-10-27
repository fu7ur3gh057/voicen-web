from django.db import models

from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Room(models.Model):
    user = models.OneToOneField(User, related_name='room', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="invited_rooms", verbose_name=_("Members"), blank=True)
    blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} Room'


class Message(TimeStampedUUIDModel):
    room = models.ForeignKey(Room, verbose_name=_("Room"), related_name="message_list", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("Owner"), related_name="message_list", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self):
        return f'Message {self.room}'
