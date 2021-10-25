from django.urls import path

from . import views


urlpatterns = [
    path(
        "video-token/", views.VideoChatTokenCreateAPIView.as_view(), name="video_token"
    )
]
