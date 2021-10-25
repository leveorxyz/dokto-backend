from rest_framework import serializers


class VideoChatTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    room_name = serializers.CharField(max_length=30)
