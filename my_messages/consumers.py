from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.auth import login
import json

from .models import Channel, Message
from .serializers import MessageCreateSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.channel_id = int(self.scope['url_route']['kwargs']['channel_id'])
        self.user = self.scope["user"]
        self.room_group_name = 'chat_%s' % self.channel_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("say smth")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("fafga")
        serializer = MessageCreateSerializer(data=text_data_json)
        if serializer.is_valid():
            valid_data = serializer.data
            new_data = {
                'message': valid_data['message'],
                'user': self.user,
                'channel': Channel.objects.get(id=self.channel_id)
            }
            created_message = Message.objects.create(**new_data)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': created_message.message,
                    'username': created_message.user.username,
                    'timestamp': str(created_message.timestamp)
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
