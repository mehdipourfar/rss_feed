import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rss_feed.settings')

app = Celery('rss_feed')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'trigger_update_channels': {
        'task': 'rss.tasks.trigger_update_channels',
        'schedule': 60 * 60,
        'args': ()
    },
}
