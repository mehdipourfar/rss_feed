from rest_framework.test import APITestCase

from user.tests.factories import UserFactory
from .factories import ChannelFactory, EntryFactory
from rss.models import Comment, Entry
from .mock_server import RSSMockServer


class ChannelViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = RSSMockServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.server.shutdown()

    def test_list(self):
        channels_api = '/api/channels/'

        # test unauthorized access
        response = self.client.get(channels_api)
        self.assertEqual(response.status_code, 401)

        # authorized_access
        user = UserFactory()
        for i in range(5):
            ChannelFactory()

        self.client.force_authenticate(user=user)
        response = self.client.get(channels_api)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 5)

        included_fields = [
            'id',
            'title',
            'description',
            'link',
            'image_url',
            'subscribed',
            'unread_entries_count',
        ]
        item = data['results'][0]

        for field in included_fields:
            with self.subTest(field=field):
                self.assertIn(field, item)

    def test_subscribe_unsubscribe(self):
        channel = ChannelFactory()
        channel_api = f'/api/channels/{channel.id}/'

        user = UserFactory()
        self.client.force_authenticate(user=user)

        # by default, users are unsubscribed
        response = self.client.get(channel_api)
        self.assertFalse(response.json()['subscribed'])

        # add subscription
        response = self.client.post(f'/api/channels/{channel.id}/subscribe/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(channel_api)
        self.assertTrue(response.json()['subscribed'])

        # remove subscription
        response = self.client.post(f'/api/channels/{channel.id}/unsubscribe/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(channel_api)
        self.assertFalse(response.json()['subscribed'])

    def test_subscribed_channels_filter(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        channels = [ChannelFactory() for i in range(3)]
        channels[0].subscribers.add(user)
        response = self.client.get('/api/channels/')
        self.assertEqual(response.json()['count'], 3)
        response = self.client.get('/api/channels/?subscribed=true')
        self.assertEqual(response.json()['count'], 1)
        response = self.client.get('/api/channels/?subscribed=false')
        self.assertEqual(response.json()['count'], 2)

    def test_unread_entries_count(self):
        channel = ChannelFactory()
        channel_api = f'/api/channels/{channel.id}/'
        entries = [EntryFactory(channel=channel) for i in range(5)]

        user = UserFactory()
        user_2 = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(channel_api)
        self.assertEqual(response.json()['unread_entries_count'], 5)

        entries[0].read_by.add(user)
        entries[1].read_by.add(user_2)
        entries[2].read_by.add(user_2)

        response = self.client.get(channel_api)
        self.assertEqual(response.json()['unread_entries_count'], 4)

        self.client.force_authenticate(user=user_2)
        response = self.client.get(channel_api)
        self.assertEqual(response.json()['unread_entries_count'], 3)

    def test_register_channel(self):
        user = UserFactory()
        self.client.force_authenticate(user)
        response = self.client.post(
            '/api/channels/register_channel/',
            {'link': f'{self.server.address}/rss'}
        )
        self.assertEqual(response.status_code, 200)
        channel_id = response.json()['id']
        entries_count = Entry.objects.filter(channel_id=channel_id).count()
        self.assertEqual(entries_count, 103)


class EntryViewSetTestCase(APITestCase):
    def test_list(self):
        channel_1 = ChannelFactory()
        channel_2 = ChannelFactory()

        for i in range(4):
            EntryFactory(channel=channel_1)

        for i in range(2):
            EntryFactory(channel=channel_2)

        user = UserFactory()
        response = self.client.get('/api/entries/')
        self.assertEqual(response.status_code, 401)
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/entries/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 6)

        response = self.client.get(f'/api/entries/?channel_id={channel_1.id}')
        data = response.json()
        self.assertEqual(data['count'], 4)

        included_fields = [
            'title',
            'link',
            'description',
            'image_url',
            'category',
            'publish_date',
            'author',
            'marked',
            'read'
        ]
        item = data['results'][0]

        for field in included_fields:
            with self.subTest(field=field):
                self.assertIn(field, item)

    def test_read_unread(self):
        entry = EntryFactory()
        entry_api = f'/api/entries/{entry.id}/'

        user = UserFactory()
        self.client.force_authenticate(user=user)

        # by default, entries are unread
        response = self.client.get(entry_api)
        self.assertFalse(response.json()['read'])

        # add subscription
        response = self.client.post(f'/api/entries/{entry.id}/read/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(entry_api)
        self.assertTrue(response.json()['read'])

        # remove subscription
        response = self.client.post(f'/api/entries/{entry.id}/unread/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(entry_api)
        self.assertFalse(response.json()['read'])

    def test_mark_unmark(self):
        entry = EntryFactory()
        entry_api = f'/api/entries/{entry.id}/'

        user = UserFactory()
        self.client.force_authenticate(user=user)

        # by default, entries are unread
        response = self.client.get(entry_api)
        self.assertFalse(response.json()['read'])

        # add subscription
        response = self.client.post(f'/api/entries/{entry.id}/mark/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(entry_api)
        self.assertTrue(response.json()['marked'])

        # remove subscription
        response = self.client.post(f'/api/entries/{entry.id}/unmark/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(entry_api)
        self.assertFalse(response.json()['marked'])

    def test_filters(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        channel = ChannelFactory()
        entries = [EntryFactory(channel=channel) for i in range(5)]
        for entry in entries[:2]:
            entry.read_by.add(user)

        entries[4].marked_by.add(user)

        response = self.client.get(
            f'/api/entries/?channel_id={channel.id}&read=true'
        )
        self.assertEqual(response.json()['count'], 2)
        response = self.client.get(
            f'/api/entries/?channel_id={channel.id}&marked=true'
        )
        self.assertEqual(response.json()['count'], 1)


class CommentTestCase(APITestCase):
    def test_comment(self):
        entry = EntryFactory()
        user = UserFactory()

        self.client.force_authenticate(user=user)
        response = self.client.post(
            f'/api/entries/{entry.id}/comments/',
            {'body': 'hey hey'}
        )
        self.assertEqual(response.status_code, 201)

        # update comment
        comment_id = response.json()['id']
        response = self.client.patch(
            f'/api/entries/{entry.id}/comments/{comment_id}/',
            {'body': 'ha ha'}
        )
        comment = Comment.objects.get()
        self.assertEqual(comment.body, 'ha ha')

        # test user only view his comments
        user_2 = UserFactory()
        Comment.objects.create(body='hoo hoo',
                               entry_id=entry.id,
                               user=user_2)

        response = self.client.get(
            f'/api/entries/{entry.id}/comments/',
            {'body': 'hey hey'}
        )
        self.assertEqual(response.json()['count'], 1)
