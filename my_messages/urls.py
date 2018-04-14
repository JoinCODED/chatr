from django.urls import path
from .views import (
    MessageCreateView,
    MessageListView,
    UserLoginAPIView,
    UserCreateAPIView
)
urlpatterns = [
    path('', MessageListView.as_view(), name='message-list'),
    path('create/', MessageCreateView.as_view(), name='message-create'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
]
