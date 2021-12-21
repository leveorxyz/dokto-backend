import os
from datetime import datetime
from django.utils.text import get_valid_filename
from rest_framework import serializers

from user.models import User
from .models import WaitingRoom


class VideoChatTokenSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    room_name = serializers.CharField(max_length=30)


class AppointmentVideoChatTokenSerializer(serializers.Serializer):
    identity = serializers.CharField()


class CreateConversessionSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField(required=False)
    doctor_username = serializers.CharField(required=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.context["request"].user.user_type == User.UserType.DOCTOR:
            if "patient_id" not in data:
                raise serializers.ValidationError("patient_id is required")

        if self.context["request"].user.user_type == User.UserType.PATIENT:
            if "doctor_username" not in data:
                raise serializers.ValidationError("doctor_username is required")

        return data


class ConversationaRemoveParticipantSerializer(serializers.Serializer):
    channel_unique_name = serializers.CharField()


class VideoRemoveParticipantSerializer(serializers.Serializer):
    room_name = serializers.CharField()
    participant_sid = serializers.CharField()


class WaitingRoomSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        room_media = validated_data.get("room_media", None)
        if room_media:
            if instance.room_media.name:
                os.remove(instance.room_media.path)
            mime_type = room_media.content_type
            if mime_type.startswith("video/"):
                validated_data["text"] = None
            instance.room_media_mime_type = mime_type
        else:
            instance.room_media_mime_type = None
        instance.save()
        return super().update(instance, validated_data)

    class Meta:
        model = WaitingRoom
        exclude = ("created_at", "updated_at", "is_deleted", "deleted_at", "doctor")
        extra_kwargs = {"room_media_mime_type": {"read_only": True}}
