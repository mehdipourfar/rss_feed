import calendar
import datetime
import time

from django.utils import timezone
from django.conf import settings


def time_struct_to_timestamptz(time_struct):
    t = time.mktime(time_struct)
    dt = datetime.datetime.fromtimestamp(t)
    return timezone.make_aware(dt)


def unix_timestamp(timestamp, milisecond=True):
    if hasattr(timestamp, 'timestamp'):
        timestamp = timestamp.timestamp()
    else:
        timestamp = calendar.timegm(timestamp.timetuple())

    if milisecond:
        timestamp *= 1000
    return int(timestamp)


def run_task(task, **kwargs):
    eta = kwargs.pop('eta', None)
    if settings.TEST_IS_RUNNING:
        task(**kwargs)
    else:
        task.apply_async(kwargs=kwargs, eta=eta)
