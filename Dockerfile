FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
        apt-get install --no-install-recommends -y lsb-release wget sudo gnupg1 \
        && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
        && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
        && apt-get update \
        && apt-get install --no-install-recommends -y postgresql-client-12
RUN pip install --no-cache-dir -U pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get autoremove -y
RUN apt-get clean
COPY . /rss_feed
WORKDIR /rss_feed
VOLUME /rss_shared_dir
ENV DJANGO_SETTINGS_MODULE=rss_feed.settings.production
