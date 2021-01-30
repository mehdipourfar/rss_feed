from rest_framework import serializers
from .models import Channel, Entry, Comment

from utils.funcs import unix_timestamp


class ChannelSerializer(serializers.ModelSerializer):
    # These values are annotated by viewset's queryset
    subscribed = serializers.SerializerMethodField()
    unread_entries_count = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = (
            'id',
            'title',
            'description',
            'link',
            'image_url',
            'subscribed',
            'unread_entries_count',
        )

    def get_subscribed(self, obj):
        if hasattr(obj, 'subscribed'):
            return obj.subscribed
        user = self.context['request'].user
        return obj.subscribers.filter(id=user.id).exists()

    def get_unread_entries_count(self, obj):
        if hasattr(obj, 'unread_entries_count'):
            return obj.unread_entries_count
        user = self.context['request'].user
        return user.read_entries.filter(
            channel_id=obj.id
        ).count()


class EntrySerializer(serializers.ModelSerializer):
    publish_date = serializers.SerializerMethodField()

    # These values are annotated by viewset's queryset
    marked = serializers.SerializerMethodField()
    read = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = (
            'title',
            'link',
            'description',
            'image_url',
            'category',
            'publish_date',
            'author',
            'marked',
            'read'
        )

    def get_publish_date(self, obj):
        return unix_timestamp(obj.publish_date)

    def get_marked(self, obj):
        if hasattr(obj, 'marked'):
            return obj.marked
        user = self.context['request'].user
        return user.marked_entries.filter(
            entry=obj
        ).exists()

    def get_read(self, obj):
        if hasattr(obj, 'read'):
            return obj.read
        user = self.context['request'].user
        return user.read_entries.filter(
            entry=obj
        ).exists()


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    entry_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'entry_id',
            'user_id',
            'created_at',
            'body',
        )

    def get_created_at(self, obj):
        return unix_timestamp(obj.created_at)


class LinkSerializer(serializers.Serializer):
    link = serializers.URLField()
