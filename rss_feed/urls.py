from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import rss.views
import user.views


router = routers.DefaultRouter()
router.register(r'channels', rss.views.ChannelViewSet, basename='channels')
router.register(r'users', user.views.UserViewSet, basename='users')
router.register(r'entries/(?P<entry_id>\d+)/comments',
                rss.views.CommentViewSet,
                basename='comments')
router.register(r'entries',
                rss.views.EntryViewSet,
                basename='entries')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
