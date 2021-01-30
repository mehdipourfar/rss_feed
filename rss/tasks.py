from celery import shared_task

from .models import Channel, Entry
from .utils import crawl_and_parse
from utils.funcs import run_task


@shared_task
def trigger_update_channels():
    for channel_id in Channel.objects.values_list('id', flat=True):
        run_task(update_channel, channel_id=channel_id)


@shared_task
def update_channel(channel_id):
    channel = Channel.objects.get(id=channel_id)
    data = crawl_and_parse(channel.link)
    if channel.last_update == data['channel']['last_update']:
        return

    entries = [Entry(channel_id=channel_id, **fields)
               for fields in data['entries']]
    Entry.objects.bulk_create(entries, ignore_conflicts=True)
    Channel.objects.filter(id=channel.id).update(
        **data['channel']
    )
