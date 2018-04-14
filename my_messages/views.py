from .serializers import (
    MessageListSerializer,
    MessageCreateSerializer,
    UserCreateSerializer,
    UserLoginSerializer
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import Message

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

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

class MessageCreateView(CreateAPIView):
    serializer_class = MessageCreateSerializer

class MessageListView(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all()
        latest = request.GET.get('latest')
        if latest:
            messages = messages.filter(timestamp__gt=latest)

        message_list = MessageListSerializer(messages, many=True).data

        return Response(message_list, status=status.HTTP_200_OK)
