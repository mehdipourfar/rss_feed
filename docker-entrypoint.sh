#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
export DJANGO_SETTINGS_MODULE=rss_feed.settings.production
exec gunicorn --workers 4 \
         --bind 0.0.0.0:8080 \
         --pythonpath=/rss_feed \
         rss_feed.wsgi:application
