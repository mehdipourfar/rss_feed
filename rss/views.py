from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Channel, Entry, Comment
from .serializers import (
    LinkSerializer,
    ChannelSerializer,
    EntrySerializer,
    CommentSerializer
)
from .filters import ChannelFilter, EntryFilter
from .tasks import update_channel
from utils.funcs import run_task


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer
    filter_class = ChannelFilter

    def get_queryset(self):
        user = self.request.user
        return (Channel.objects
                .annotate_subscribed(user)
                .annotate_unread_entries_count(user))

    @action(methods=['POST'], detail=True)
    def subscribe(self, request, pk):
        channel = self.get_object()
        channel.subscribers.add(request.user)
        return Response(status=204)

    @action(methods=['POST'], detail=True)
    def unsubscribe(self, request, pk):
        channel = self.get_object()
        channel.subscribers.remove(request.user)
        return Response(status=204)

    @action(methods=['POST'], detail=True)
    def update_entries(self, request, pk):
        channel = self.get_object()
        run_task(update_channel, channel_id=channel.id)
        return Response(status=204)

    @action(methods=['POST'], detail=False)
    def register_channel(self, request):
        serializer = LinkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        channel, _ = Channel.objects.get_or_create(
            link=serializer.data['link']
        )
        serializer = ChannelSerializer(channel, context={'request': request})
        run_task(update_channel, channel_id=channel.id)
        return Response(serializer.data)


class EntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EntrySerializer
    filter_class = EntryFilter

    def get_queryset(self):
        user = self.request.user
        return (Entry.objects
                .annotate_marked(user)
                .annotate_read(user))

    def list(self, request, *args, **kwargs):
        if 'channel_id' not in request.query_params:
            raise ValidationError({
                'error': 'channel_id querystring is required'
            })
        return super().list(request, *args, **kwargs)

    @action(methods=['POST'], detail=True)
    def read(self, request, pk):
        entry = self.get_object()
        entry.read_by.add(request.user)
        return Response(status=204)

    @action(methods=['POST'], detail=True)
    def unread(self, request, pk):
        entry = self.get_object()
        entry.read_by.remove(request.user)
        return Response(status=204)

    @action(methods=['POST'], detail=True)
    def mark(self, request, pk):
        entry = self.get_object()
        entry.marked_by.add(request.user)
        return Response(status=204)

    @action(methods=['POST'], detail=True)
    def unmark(self, request, pk):
        entry = self.get_object()
        entry.marked_by.remove(request.user)
        return Response(status=204)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            entry_id=self.kwargs.get('entry_id'),
            user=self.request.user,
        )
