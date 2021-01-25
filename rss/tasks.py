from datetime import timedelta

from celery import shared_task
from celery.decorators import periodic_task
from django.conf import settings

from .models import Channel, Entry
from .feed import crawl_and_parse
from utils.funcs import run_task


@periodic_task(run_every=timedelta(minutes=settings.CHANNELS_REFRESH_INTERVAL))
def trigger_update_channels():
    for channel_id in Channel.objects.values_list('id', flat=True):
        run_task(update_channel, channel_id=channel_id)


@shared_task
def update_channel(channel_id):
    channel = Channel.objects.get(channel_id)
    results = crawl_and_parse(channel.link)
    entries = [Entry(channel_id=channel_id, **result)
               for result in results]
    Entry.objects.bulk_create(entries, ignore_conflicts=True)
