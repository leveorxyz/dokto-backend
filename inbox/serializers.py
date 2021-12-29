from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, SerializerMethodField, UUIDField
from rest_framework.serializers import ModelSerializer, Serializer
from django.db.models import Q

from .models import InboxChannel, InboxMessage
from core.serializers import ReadWriteSerializerMethodField
from user.models import User


class InboxUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "profile_photo"]
        extra_kwargs = {
            "full_name": {"read_only": True},
            "profile_photo": {"read_only": True},
        }


class InboxChannelPostSchemaSerializer(Serializer):
    second_user = UUIDField(required=True)
    encounter_reason = CharField(required=False, allow_blank=True)

    class Meta:
        fields = ["second_user", "encounter_reason"]


class InboxChannelSerializer(ModelSerializer):
    first_user = ReadWriteSerializerMethodField()
    second_user = ReadWriteSerializerMethodField()
    unread_count = SerializerMethodField()

    def get_first_user(self, obj):
        return InboxUserSerializer(obj.first_user).data

    def get_second_user(self, obj):
        return InboxUserSerializer(obj.second_user).data

    def get_unread_count(self, obj) -> int:
        return obj.get_unread_msg_count(self.context["request"].user)

    def validate(self, attrs):
        data = super().validate(attrs)
        if InboxChannel.objects.filter(
            Q(first_user=data["first_user"].id, second_user=data["second_user"].id)
            | Q(first_user=data["second_user"].id, second_user=data["first_user"].id)
        ).exists():
            raise ValidationError("Channel already exists")
        return data

    def create(self, validated_data):
        return InboxChannel.objects.create(**validated_data)

    class Meta:
        model = InboxChannel
        fields = ("id", "first_user", "second_user", "encounter_reason", "unread_count")


class InboxMessageSerializer(ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not InboxChannel.objects.filter(
            Q(first_user=self.context["request"].user)
            | Q(second_user=self.context["request"].user)
        ).exists():
            raise ValidationError("You are not in this channel")
        return data

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        message = InboxMessage.from_validated_data(validated_data)
        if "uploaded_file" in validated_data:
            file = validated_data.get("uploaded_file")
            message.uploaded_file_mimetype = file.content_type
        message.save()
        return message

    class Meta:
        model = InboxMessage
        fields = [
            "channel",
            "message",
            "subject",
            "sender",
            "read_status",
            "uploaded_file",
            "uploaded_file_mimetype",
        ]
        extra_kwargs = {
            "channel": {"required": True},
            "message": {"required": True},
            "subject": {"required": False},
            "read_status": {"read_only": True},
            "sender": {"read_only": True},
            "uploaded_file": {"required": False},
            "uploaded_file_mimetype": {"read_only": True},
        }


class InboxChannelMessage(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.sender != self.context["request"].user:
            instance.read_status = True
            instance.save()
        return data

    class Meta:
        model = InboxMessage
        fields = ["channel", "message", "subject", "sender", "read_status"]
        extra_kwargs = {
            "channel": {"required": True},
            "message": {"required": True},
            "subject": {"required": False},
            "read_status": {"read_only": True},
        }
