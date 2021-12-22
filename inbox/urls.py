from django.urls import path

from . import views

urlpatterns = [
    path("", views.InboxChannelListView.as_view(), name="inbox-channel-list"),
    path(
        "send-message/",
        views.InboxSendMessageAPIView.as_view(),
        name="inbox-send-message",
    ),
]
