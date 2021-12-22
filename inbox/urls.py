from django.urls import path

from . import views

urlpatterns = [
    path("", views.InboxChannelListView.as_view(), name="inbox-channel-list"),
]
