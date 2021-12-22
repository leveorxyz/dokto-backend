from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, IntegerField

from .models import InboxChannel


class InboxChannelSerializer(ModelSerializer):
    unread_count = SerializerMethodField()

    def get_unread_count(self, obj):
        return obj.get_unread_msg_count(self.context["request"].user)

    class Meta:
        model = InboxChannel
        fields = ("id", "first_user", "second_user", "unread_count")
