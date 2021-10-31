from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.views import (
    CustomRetrieveAPIView,
    CustomRetrieveUpdateAPIView,
    CustomListUpdateAPIView,
)
from core.permissions import OwnProfilePermission
from user.models import DoctorInfo, User
from core.utils import set_user_ip
from core.views import custom_response
from .serializers import (
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorSpecialtySettingsSerializer,
    DoctorExperienceEducationSerializer,
    DoctorExperienceEducationUpdateSerializer,
    DoctorAvailableHoursSerializerWithID,
    DoctorAvailableHoursUpdateSerializerWithID,
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
    permission_classes = [IsAuthenticated, OwnProfilePermission]
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
    permission_classes = [IsAuthenticated, OwnProfilePermission]
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
    permission_classes = [IsAuthenticated, OwnProfilePermission]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return DoctorAvailableHoursUpdateSerializerWithID
        else:
            return DoctorAvailableHoursSerializerWithID

    def get_queryset(self):
        doctor_info = get_object_or_404(
            DoctorInfo, user__username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, doctor_info)
        return doctor_info.doctoravailablehours_set.all()

    def perform_update(self, serializer):
        serializer.validated_data[
            "doctor_info"
        ] = self.request.user.doctorinfo_set.first()
        serializer.update(serializer.instance, serializer.validated_data)


class DoctorSpecialtySettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = DoctorSpecialtySettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj
