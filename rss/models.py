from urllib.parse import urlparse

from django.db import models


class Channel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    link = models.URLField()
    image_url = models.URLField(default='', blank=True)

    @property
    def domain(self):
        return urlparse(self.link).netloc

    def __str__(self):
        return self.title or self.domain


class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=500)
    link = models.URLField()
    description = models.TextField(default='')
    image_url = models.URLField(default='', blank=True)
    category = models.TextField(default='')
    publish_date = models.DateTimeField()
    author = models.TextField(default='')

    class Meta:
        unique_together = (
            'channel', 'link'
        )

    def __str__(self):
        return self.title
