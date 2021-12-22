from django.db.models import Q

from core.views import CustomListAPIView
from .models import InboxChannel
from .serializers import InboxChannelSerializer

# Create your views here.


class InboxChannelListView(CustomListAPIView):
    serializer_class = InboxChannelSerializer

    def get_queryset(self):
        user = self.request.user
        return InboxChannel.objects.filter(Q(first_user=user) | Q(second_user=user))
