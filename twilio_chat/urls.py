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
    path(
        "create-conversation/",
        views.CreateConversationAPIView.as_view(),
        name="create_conversation",
    ),
    path(
        "add-participant-conversation/",
        views.ConversationAddParticipantAPIView.as_view(),
        name="add_participant_conversation",
    ),
    path(
        "remove-participant-conversation/",
        views.ConversationRemoveParticipantAPIView.as_view(),
        name="remove_participant_conversation",
    ),
    path(
        "delete-conversation/",
        views.DeleteConversationAPIView.as_view(),
        name="conversation_delete",
    ),
]
