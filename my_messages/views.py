from .serializers import (
    MessageListSerializer,
    MessageCreateSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    ChannelSerializer,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import Message, Channel

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.permissions import (AllowAny, IsAuthenticated)

from django.http import HttpResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class ChannelCreateAPIView(CreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
    permission_classes = [AllowAny, ]


class MessageCreateView(APIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, channel_id):
        my_data = request.data
        serializer = self.serializer_class(data=my_data)
        if serializer.is_valid():
            valid_data = serializer.data
            new_data = {
                'message': valid_data['message'],
                'user': request.user,
                'channel': Channel.objects.get(id=channel_id)
            }
            created_message = Message.objects.create(**new_data)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'chat_%s' % channel_id,
                {
                    'type': 'chat_message',
                    'message': created_message.message,
                    'username': created_message.user.username,
                    'timestamp': str(created_message.timestamp)
                }
            )
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MessageListView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, channel_id):
        messages = Message.objects.filter(
            channel=Channel.objects.get(id=channel_id))
        latest = request.GET.get('latest')
        if latest:
            messages = messages.filter(timestamp__gt=latest)

        message_list = MessageListSerializer(messages, many=True).data

        return Response(message_list, status=status.HTTP_200_OK)


def deleteTheHamza(request):
    Message.objects.filter(user__username="hamsa").delete()
    return HttpResponse("LOOOOL")
