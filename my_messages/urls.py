from django.urls import path
from .views import (
    MessageCreateView,
    MessageListView,
    UserLoginAPIView,
    UserCreateAPIView,
    ChannelCreateAPIView,
    ChannelListAPIView
)
urlpatterns = [
    path('', ChannelListAPIView.as_view(), name='channel-list'),
    path('create/', ChannelCreateAPIView.as_view(), name='channel-create'),
    path('<int:channel_id>/', MessageListView.as_view(), name='message-list'),
    path('<int:channel_id>/create/', MessageCreateView.as_view(), name='message-create'),
]
