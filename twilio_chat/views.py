from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant

from django.conf import settings


from .serializers import (
    VideoChatTokenSerializer,
    AppointmentVideoChatTokenSerializer,
    CreateConversessionSerializer,
)
from user.models import User, DoctorInfo, PatientInfo


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
        token.add_grant(ChatGrant(service_sid=settings.TWILIO_CONVERSATION_SERVICE_SID))

        data = {
            "status_code": 201,
            "message": "Success",
            "result": {
                "token": token.to_jwt(),
                "identity": token.identity,
            },
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class CreateConversationAPIView(generics.CreateAPIView):
    """
    View for handling twilio video chat access token generation.
    """

    serializer_class = CreateConversessionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        patient_user: User = None
        doctor_user: User = None

        if self.request.user.user_type == User.UserType.DOCTOR:
            unique_name = f"{self.request.user.id}_{validated_data['patient_id']}"
            patient_user = User.objects.get(id=validated_data["patient_id"])
            friendly_name = patient_user.full_name
            doctor_user = self.request.user

        if self.request.user.user_type == User.UserType.PATIENT:
            doctor = DoctorInfo.objects.get(username=validated_data["doctor_username"])
            unique_name = f"{doctor.user.id}_{self.request.user.id}"
            friendly_name = self.request.user.full_name
            validated_data["patient_id"] = self.request.user.id
            patient_user = self.request.user
            doctor_user = doctor.user

        validated_data.update(
            {
                "friendly_name": friendly_name,
                "unique_name": unique_name,
            }
        )

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        service = client.conversations.services(
            settings.TWILIO_CONVERSATION_SERVICE_SID
        )
        try:
            conversation = service.conversations.create(
                friendly_name=validated_data.get("friendly_name"),
                unique_name=validated_data.get("unique_name"),
                state="active",
            )
        except TwilioRestException as e:
            conversation = client.conversations.conversations(
                validated_data.get("unique_name")
            ).fetch()
        participant_unique_names = [
            f"{patient_user.id}_{patient_user.full_name}",
            f"{doctor_user.id}_{doctor_user.full_name}",
        ]
        print(participant_unique_names)
        participant_data = []
        for participant_name in participant_unique_names:
            try:
                participant = service.conversations(
                    conversation.sid
                ).participants.create(identity=participant_name)
            except TwilioRestException as e:
                return Response(
                    data={"status_code": 400, "message": e.msg, "result": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            participant_data.append(participant._properties)
        return Response(
            data={
                "status_code": 201,
                "message": "Success",
                "result": {
                    "channel": conversation._properties,
                    "participants": participant_data,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class DeleteConversationAPIView(APIView):
    """
    View for handling twilio video chat access token generation.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        service = client.conversations.services(
            settings.TWILIO_CONVERSATION_SERVICE_SID
        )
        conversation_list = service.conversations.list()
        for conversation in conversation_list:
            conversation.delete()
        return Response(
            data={"status_code": 200, "message": "Success", "result": None},
            status=status.HTTP_201_CREATED,
        )
