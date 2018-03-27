from rest_framework import serializers
from .models import Message

class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['timestamp',]
