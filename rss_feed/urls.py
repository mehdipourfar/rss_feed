from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import rss.views
import user.views


router = routers.DefaultRouter()
router.register(r'channels', rss.views.ChannelViewSet, basename='channels')
router.register(r'users', user.views.UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
