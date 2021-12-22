from django.db.models import Q
from rest_framework.generics import get_object_or_404

from core.views import CustomCreateAPIView, CustomListAPIView
from .models import InboxChannel, InboxMessage
from .serializers import (
    InboxChannelSerializer,
    InboxMessageSerializer,
    InboxChannelMessage,
)

# Create your views here.


class InboxChannelListView(CustomListAPIView):
    serializer_class = InboxChannelSerializer

    def get_queryset(self):
        user = self.request.user
        return InboxChannel.objects.filter(Q(first_user=user) | Q(second_user=user))


class InboxSendMessageAPIView(CustomCreateAPIView):
    serializer_class = InboxMessageSerializer
    queryset = InboxMessage.objects.all()


class InboxReadMessageAPIView(CustomListAPIView):
    serializer_class = InboxChannelMessage

    def get_queryset(self):
        return InboxMessage.objects.filter()

    def get_object(self, channel_id):
        return get_object_or_404(self.get_queryset(), channel_id=channel_id)


class InboxCreateChannelAPIView(CustomCreateAPIView):
    serializer_class = InboxChannelSerializer
    queryset = InboxChannel.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method.upper() == "POST":
            self.request.data["first_user"] = self.request.user.id
        return super().get_serializer(*args, **kwargs)
