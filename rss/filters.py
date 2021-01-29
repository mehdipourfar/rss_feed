import django_filters

from .models import Channel, Entry


class ChannelFilter(django_filters.FilterSet):
    subscribed = django_filters.BooleanFilter(
        method='filter_subscribed',
        widget=django_filters.widgets.BooleanWidget()
    )

    class Meta:
        model = Channel
        fields = [
            'subscribed',
        ]

    def filter_subscribed(self, qs, name, value):
        return qs.filter(subscribed=value) if value is not None else qs


class EntryFilter(django_filters.FilterSet):
    channel_id = django_filters.NumberFilter(method='filter_channel_id')
    read = django_filters.BooleanFilter(
        method='filter_read',
        widget=django_filters.widgets.BooleanWidget()
    )
    marked = django_filters.BooleanFilter(
        method='filter_marked',
        widget=django_filters.widgets.BooleanWidget()
    )

    class Meta:
        model = Entry
        fields = [
            'channel_id',
            'read',
            'marked',
        ]

    def filter_channel_id(self, qs, name, value):
        return qs.filter(channel_id=value) if value is not None else qs

    def filter_read(self, qs, name, value):
        return qs.filter(read=value) if value is not None else qs

    def filter_marked(self, qs, name, value):
        return qs.filter(marked=value) if value is not None else qs
