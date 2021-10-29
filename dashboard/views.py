from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from core.views import CustomRetrieveAPIView, CustomRetrieveUpdateAPIView
from user.models import DoctorInfo, User
from .serializers import (
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorSpecialtySettingsSerializer,
)
from .permissions import OwnProfilePermission


class DoctorProfileAPIView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer
    queryset = User.objects.filter(user_type=User.UserType.DOCTOR)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), **self.kwargs)


class DoctorProfileDetailsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [OwnProfilePermission]
    serializer_class = DoctorProfileDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorSpecialtySettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [OwnProfilePermission]
    serializer_class = DoctorSpecialtySettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get("username")
        )
        self.check_object_permissions(self.request, obj)
        return obj
