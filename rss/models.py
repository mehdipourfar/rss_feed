from urllib.parse import urlparse

from django.conf import settings
from django.db import models
from .querysets import ChannelQuerySet, EntryQuerySet


class Channel(models.Model):
    objects = ChannelQuerySet.as_manager()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(default='')
    link = models.URLField(max_length=500)
    image_url = models.URLField(default='', blank=True)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_channels',
    )

    @property
    def domain(self):
        return urlparse(self.link).netloc

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.domain
        super().save(*args, **kwargs)


class Entry(models.Model):
    objects = EntryQuerySet.as_manager()
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.PROTECT,
        related_name='entries',
    )
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=500, unique=True)
    description = models.TextField(default='')
    image_url = models.URLField(default='', blank=True)
    category = models.TextField(default='')
    publish_date = models.DateTimeField(db_index=True)
    author = models.TextField(default='')

    marked_by = models.ManyToManyField(
        'user.User',
        related_name='marked_entries',
    )
    read_by = models.ManyToManyField(
        'user.User',
        related_name='read_entries',
    )

    class Meta:
        unique_together = (
            'channel', 'link'
        )
        ordering = ('-publish_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
