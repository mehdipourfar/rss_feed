import datetime
import time

from django.utils import timezone
from django.conf import settings


def time_struct_to_timestamptz(time_struct):
    t = time.mktime(time_struct)
    dt = datetime.datetime.fromtimestamp(t)
    return timezone.make_aware(dt)


def run_task(task, **kwargs):
    eta = kwargs.pop('eta', None)
    if settings.TEST_IS_RUNNING:
        task(**kwargs)
    else:
        task.apply_async(kwargs=kwargs, eta=eta)
