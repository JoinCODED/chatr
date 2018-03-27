from .serializers import (
    MessageListSerializer,
    MessageCreateSerializer,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import Message

class MessageCreateView(CreateAPIView):
    serializer_class = MessageCreateSerializer

class MessageListView(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all()
        latest = request.GET.get('latest')
        if latest:
            messages = messages.filter(timestamp__gte=latest)

        message_list = MessageListSerializer(messages, many=True).data

        return Response(message_list, status=status.HTTP_200_OK)
