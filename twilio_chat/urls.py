from django.urls import path

from . import views


urlpatterns = [
    path(
        "video-token/", views.VideoChatTokenCreateAPIView.as_view(), name="video_token"
    ),
    path(
        "appointment-video-token/",
        views.AppointmentVideoChatTokenCreateAPIView.as_view(),
        name="appointment_video_token",
    ),
]
