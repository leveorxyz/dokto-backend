from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.views import CustomRetrieveAPIView, CustomRetrieveUpdateAPIView
from core.permissions import OwnProfilePermission
from user.models import DoctorInfo, User
from .serializers import (
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorSpecialtySettingsSerializer,
    DoctorExperienceEducationSerializer,
    DoctorExperienceEducationUpdateSerializer,
)


class DoctorProfileAPIView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer
    queryset = User.objects.filter(user_type=User.UserType.DOCTOR)

    def get_object(self) -> DoctorInfo:
        return get_object_or_404(self.get_queryset(), **self.kwargs)


class DoctorProfileDetailsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = DoctorProfileDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get("username")
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
            self.get_queryset(), user__username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorSpecialtySettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = DoctorSpecialtySettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj
