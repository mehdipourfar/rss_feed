import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from rss.models import Channel, Entry


class ChannelFactory(DjangoModelFactory):
    class Meta:
        model = Channel

    link = factory.Sequence(lambda n: f'http://www.site{n}.com/rss')


class EntryFactory(DjangoModelFactory):
    class Meta:
        model = Entry

    channel = factory.SubFactory(ChannelFactory)
    publish_date = factory.LazyFunction(timezone.now)
    title = factory.Sequence(lambda n: f'title#{n}')
    link = factory.Sequence(lambda n: f'http://www.site.com/article/{n}')
