from celery import shared_task

from .models import Channel, Entry
from .feed import crawl_and_parse
from utils.funcs import run_task


@shared_task
def trigger_update_channels():
    for channel_id in Channel.objects.values_list('id', flat=True):
        run_task(update_channel, channel_id=channel_id)


@shared_task
def update_channel(channel_id):
    channel = Channel.objects.get(id=channel_id)
    results = crawl_and_parse(channel.link)
    entries = [Entry(channel_id=channel_id, **result)
               for result in results]
    Entry.objects.bulk_create(entries, ignore_conflicts=True)
