from rest_framework.serializers import ModelSerializer

from .models import InboxChannel


class InboxChannelSerializer(ModelSerializer):
    class Meta:
        model = InboxChannel
        fields = "__all__"
