from django.urls import path

from . import views

urlpatterns = [
    path("channel/", views.InboxChannelListView.as_view(), name="inbox-channel-list"),
    path(
        "channel/create/",
        views.InboxCreateChannelAPIView.as_view(),
        name="inbox-channel-create",
    ),
    path(
        "send-message/",
        views.InboxSendMessageAPIView.as_view(),
        name="inbox-send-message",
    ),
    path(
        "read-message/<uuid:channel_id>/",
        views.InboxReadMessageAPIView.as_view(),
        name="inbox-read-message",
    ),
]
