from django.urls import path
from .views import (
    MessageCreateView,
    MessageListView
)
urlpatterns = [
    path('', MessageListView.as_view(), name='message-list'),
    path('create/', MessageCreateView.as_view(), name='message-create'),
]
