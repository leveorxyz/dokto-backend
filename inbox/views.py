from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_serializer,
    OpenApiExample,
)

from core.views import CustomCreateAPIView, CustomListAPIView
from user.models import User
from .models import InboxChannel, InboxMessage
from .serializers import (
    InboxChannelPostSchemaSerializer,
    InboxChannelSerializer,
    InboxMessageSerializer,
    InboxChannelMessage,
    InboxUserSerializer,
)

# Create your views here.


class InboxChannelListView(CustomListAPIView):
    serializer_class = InboxChannelSerializer

    @extend_schema(
        request=InboxChannelPostSchemaSerializer,
        responses={
            200: OpenApiResponse(
                description="Successfully created channel",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "first_user": {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "full_name": "string",
                                    "profile_photo": "string",
                                },
                                "second_user": {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "full_name": "string",
                                    "profile_photo": "string",
                                },
                                "encounter_reason": "string",
                                "unread_count": 0,
                            }
                        ],
                    )
                ],
                response=OpenApiTypes.ANY,
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @extend_schema(
        request=InboxChannelPostSchemaSerializer,
        responses={
            200: OpenApiResponse(
                description="Successfully created channel",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value={
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "first_user": {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "full_name": "string",
                                "profile_photo": "string",
                            },
                            "second_user": {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "full_name": "string",
                                "profile_photo": "string",
                            },
                            "encounter_reason": "string",
                            "unread_count": 0,
                        },
                    )
                ],
                response=OpenApiTypes.ANY,
            )
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        if self.request.method.upper() == "POST":
            second_user = None
            try:
                second_user = User.objects.get(id=self.request.data["second_user"])
            except User.DoesNotExist:
                raise ValidationError("Invalid Second User")
            self.request.data["first_user"] = self.request.user
            self.request.data["second_user"] = second_user
        return super().get_serializer(*args, **kwargs)
