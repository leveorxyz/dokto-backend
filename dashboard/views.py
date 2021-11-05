from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from core.views import (
    CustomRetrieveAPIView,
    CustomRetrieveUpdateAPIView,
    CustomListUpdateAPIView,
)
from core.permissions import OwnProfilePermission, DoctorPermission
from user.models import DoctorInfo, User
from .serializers import (
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorSpecialtySettingsSerializer,
    DoctorExperienceEducationSerializer,
    DoctorExperienceEducationUpdateSerializer,
    DoctorAvailableHoursSerializerWithID,
    DoctorAvailableHoursUpdateSerializerWithID,
    DoctorAccountSettingsSerializer,
)


class DoctorProfileAPIView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer
    queryset = User.objects.filter(user_type=User.UserType.DOCTOR)

    def get_queryset(self):
        username = self.kwargs.get("username")
        doctor = get_object_or_404(DoctorInfo, username=username)
        return User.objects.filter(id=doctor.user_id)

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class DoctorProfileDetailsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorProfileDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorEducationExperienceSettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorExperienceEducationSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return DoctorExperienceEducationUpdateSerializer
        else:
            return DoctorExperienceEducationSerializer

    def get_queryset(self):
        return DoctorInfo.objects.all()

    def get_object(self) -> DoctorInfo:
        obj = get_object_or_404(
            self.get_queryset(), username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorAvailableHoursSettingsAPIView(CustomListUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return DoctorAvailableHoursUpdateSerializerWithID
        else:
            return DoctorAvailableHoursSerializerWithID

    def get_queryset(self):
        doctor_info = get_object_or_404(
            DoctorInfo, username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, doctor_info)
        return doctor_info.doctoravailablehours_set.all()

    def perform_update(self, serializer):
        serializer.validated_data[
            "doctor_info"
        ] = self.request.user.doctorinfo_set.first()
        serializer.update(serializer.instance, serializer.validated_data)


class DoctorSpecialtySettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorSpecialtySettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorAccountSettingsAPIView(CustomRetrieveUpdateAPIView):
    # TODO: create new fields in DoctorInfo: `notification_email`, `deletion_reason`, `temporary_disable`
    permission_classes = [AllowAny, DoctorPermission]
    serializer_class = DoctorAccountSettingsSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        doctor_info = get_object_or_404(DoctorInfo, user=user)
        temporary_disable = doctor_info.temporary_disable
        notification_email = doctor_info.notification_email
        data = {
            "notification_email": notification_email,
            "temporarily_disable": temporary_disable,
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    def update(self, request, *args, **kwargs):
        user = request.user
        doctor_info = get_object_or_404(DoctorInfo, user=user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if validated_data.get("reset_old_password") and validated_data.get(
            "reset_new_password"
        ):
            old_password = validated_data.pop("reset_old_password")
            new_password = validated_data.pop("reset_new_password")
            if not user.check_password(old_password):
                raise ValidationError("Incorrect password")
            else:
                password = make_password(new_password)
                user.password = password
        if validated_data.get("delete_old_password"):
            if not user.check_password(validated_data.pop("delete_old_password")):
                raise ValidationError("Incorrect password")
            else:
                user.is_active = False
                if validated_data.get("delete_reason"):
                    doctor_info.deletion_reason = validated_data.pop("delete_reason")
        if validated_data.get("notification_email"):
            doctor_info.notification_email = validated_data.pop("notification_email")
        if validated_data.get("temporarily_disable"):
            doctor_info.temporary_disable = not validated_data.pop(
                "temporarily_disable"
            )
        user.save()
        doctor_info.save()
        return Response({"message": "Updated successfully!"}, status=200)
