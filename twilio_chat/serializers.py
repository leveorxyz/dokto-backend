from rest_framework import serializers


class VideoChatTokenSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    room_name = serializers.CharField(max_length=30)


class AppointmentVideoChatTokenSerializer(serializers.Serializer):
    identity = serializers.CharField()
    room_name = serializers.ListField(child=serializers.CharField())
