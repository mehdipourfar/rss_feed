import django_filters

from .models import Entry


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
        return qs.filter(channel_id=value) if value else qs

    def filter_read(self, qs, name, value):
        return qs.filter(read=True) if value else qs

    def filter_marked(self, qs, name, value):
        return qs.filter(marked=True) if value else qs
