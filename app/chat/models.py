from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
import logging

logger = logging.getLogger('chat.views')


class Room(models.Model):
    # creator = models.ForeignKey('Artist', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=6)  # make unique
    artists = models.ManyToManyField('Artist')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


def artists_changed(instance, *args, **kwargs):
    artists_count = instance.artists.count()

    # make the room active
    if not instance.active and artists_count == 1:
        setattr(instance, 'active', True)
        logger.info(f"Room {instance.name} has activated")
        print('1')
    # close the room
    if instance.active and artists_count == 0:
        setattr(instance, 'active', False)
        logger.info(f"Room {instance.name} has deactivated")

    instance.save()


m2m_changed.connect(artists_changed, sender=Room.artists.through)


class Artist(models.Model):
    nickname = models.CharField(max_length=30, default='')

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nickname}'
