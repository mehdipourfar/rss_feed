from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Channel, Entry, Comment
from .serializers import ChannelSerializer, EntrySerializer, CommentSerializer
from .filters import EntryFilter


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer

    def get_queryset(self):
        return Channel.objects.annotate_subscribed(
            user=self.request.user
        ).annotate_unread_entries_count(
            user=self.request.user
        )

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


class EntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EntrySerializer
    filter_class = EntryFilter

    def get_queryset(self):
        return Entry.objects.annotate_marked(
            user=self.request.user
        ).annotate_read(
            user=self.request.user
        )

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

    def create(self, request, *args, **kwargs):
        data = {**request.data,
                'user_id': request.user.id,
                'entry_id': kwargs['entry_id']}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        data = {**request.data,
                'user_id': request.user.id,
                'entry_id': kwargs['entry_id']}
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
