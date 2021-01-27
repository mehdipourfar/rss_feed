from django.db import models
from django.db.models import OuterRef, Subquery, Exists, Count, F
from django.db.models.functions import Coalesce

from user.models import User


class ChannelQuerySet(models.QuerySet):
    def annotate_subscribed(self, user):
        from .models import Channel
        subscribed_channels = Channel.subscribers.through.objects.filter(
            user_id=user.id,
            channel=OuterRef('pk')
        )
        return self.annotate(
            subscribed=Exists(subscribed_channels)
        )

    def annotate_read_entries_count(self, user):
        read_entries = (
            user.read_entries
            .values('channel_id')
            .filter(channel_id=OuterRef('pk'))
            .annotate(read_count=Count('id'))
            .order_by()
            .values('read_count')
        )
        return self.annotate(
            read_entries_count=Coalesce(Subquery(read_entries[:1]), 0)
        )

    def annotate_unread_entries_count(self, user):
        return self.annotate_read_entries_count(user).annotate(
            total_entries=Count('entries')
        ).annotate(
            unread_entries_count=F('total_entries') - F('read_entries_count')
        )


class EntryQuerySet(models.QuerySet):
    def annotate_read(self, user):
        read_entries = user.read_entries.through.objects.filter(
            user=user,
            entry_id=OuterRef('pk'),
        )
        return self.annotate(
            read=Exists(read_entries)
        )

    def annotate_marked(self, user):
        marked_entries = User.marked_entries.through.objects.filter(
            user_id=user.id,
            entry=OuterRef('pk')
        )
        return self.annotate(
            marked=Exists(marked_entries)
        )
