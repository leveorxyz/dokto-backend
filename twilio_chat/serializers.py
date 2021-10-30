from rest_framework import serializers


class VideoChatTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    room_name = serializers.CharField(max_length=30)
