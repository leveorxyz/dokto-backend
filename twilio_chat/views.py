from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from django.conf import settings


from .serializers import VideoChatTokenSerializer, AppointmentVideoChatTokenSerializer


class VideoChatTokenCreateAPIView(generics.CreateAPIView):
    """
    View for handling twilio video chat access token generation.
    """

    serializer_class = VideoChatTokenSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity=validated_data.get("id"),
        )
        room = validated_data.get("room_name")
        token.add_grant(VideoGrant(room=room))

        data = {
            "status_code": 201,
            "message": "Success",
            "result": {
                "token": token.to_jwt(),
                "identity": token.identity,
                "room": room,
            },
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class AppointmentVideoChatTokenCreateAPIView(generics.CreateAPIView):
    """
    View for handling twilio video chat access token generation.
    """

    serializer_class = AppointmentVideoChatTokenSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity=validated_data.get("identity"),
        )

        token.add_grant(VideoGrant())

        data = {
            "status_code": 201,
            "message": "Success",
            "result": {
                "token": token.to_jwt(),
                "identity": token.identity,
            },
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
