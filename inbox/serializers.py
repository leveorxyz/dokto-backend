from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.db.models import Q

from .models import InboxChannel, InboxMessage


class InboxChannelSerializer(ModelSerializer):
    unread_count = SerializerMethodField()

    def get_unread_count(self, obj):
        return obj.get_unread_msg_count(self.context["request"].user)

    class Meta:
        model = InboxChannel
        fields = ("id", "first_user", "second_user", "unread_count")


class InboxSendMessageSerializer(ModelSerializer):
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
        return super().create(validated_data)

    class Meta:
        model = InboxMessage
        fields = ["channel", "message", "subject"]
