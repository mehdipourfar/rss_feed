from django.test import TestCase

from .mock_server import RSSMockServer
from .factories import ChannelFactory
from rss.tasks import update_channel


class CrawlTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = RSSMockServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.server.shutdown()

    def test_update_channel(self):
        channel = ChannelFactory(link=f'{self.server.address}/rss')
        update_channel(channel_id=channel.id)
        self.assertEqual(channel.entries.count(), 103)
