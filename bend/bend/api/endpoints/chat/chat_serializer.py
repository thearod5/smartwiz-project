from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['assistant', 'user'])
    content = serializers.CharField()


class ChatHistorySerializer(serializers.Serializer):
    messages = MessageSerializer(many=True)
