from .serializers import (
    MessageListSerializer,
    MessageCreateSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    ChannelSerializer,
)

from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import Message, Channel

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse


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
    permission_classes = [IsAuthenticated, ]


class MessageCreateView(APIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [IsAuthenticated, ]

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
            new_message = Message.objects.create(**new_data)
            return Response({
                'message': valid_data['message'],
                'username': request.user.username,
                'timestamp': new_message.timestamp
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MessageListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, channel_id):
        print(request.user.username);
        print(datetime.now())
        print(channel_id)
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
