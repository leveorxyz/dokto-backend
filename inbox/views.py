from django.db.models import Q

from core.views import CustomCreateAPIView, CustomListAPIView
from .models import InboxChannel, InboxMessage
from .serializers import InboxChannelSerializer, InboxSendMessageSerializer

# Create your views here.


class InboxChannelListView(CustomListAPIView):
    serializer_class = InboxChannelSerializer

    def get_queryset(self):
        user = self.request.user
        return InboxChannel.objects.filter(Q(first_user=user) | Q(second_user=user))


class InboxSendMessageAPIView(CustomCreateAPIView):
    serializer_class = InboxSendMessageSerializer
    queryset = InboxMessage.objects.all()
