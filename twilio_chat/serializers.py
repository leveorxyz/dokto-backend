from rest_framework import serializers

from user.models import User, DoctorInfo, PatientInfo


class VideoChatTokenSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    room_name = serializers.CharField(max_length=30)


class AppointmentVideoChatTokenSerializer(serializers.Serializer):
    identity = serializers.CharField()


class CreateConversessionSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField(required=False)
    doctor_username = serializers.CharField(required=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        unique_name = ""
        friendly_name = ""
        doctor_id = ""
        if self.context["request"].user.user_type == User.UserType.DOCTOR:
            if "patient_id" not in data:
                raise serializers.ValidationError("patient_id is required")

        if self.context["request"].user.user_type == User.UserType.PATIENT:
            if "doctor_username" not in data:
                raise serializers.ValidationError("doctor_username is required")

        return data
