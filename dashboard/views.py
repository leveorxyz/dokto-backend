from os import name
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema

from core.views import (
    CustomListCreateAPIView,
    CustomRetrieveAPIView,
    CustomRetrieveUpdateAPIView,
    CustomListUpdateAPIView,
)
from core.permissions import (
    OwnProfilePermission,
    DoctorPermission,
)
from user.models import DoctorInfo
from user.serializers import DoctorReviewSerializer
from .serializers import (
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorSpecialtySettingsSerializer,
    DoctorExperienceEducationSerializer,
    DoctorAvailableHoursSerializerWithID,
    DoctorAccountSettingsSerializer,
    DoctorProfessionalProfileSerializer,
)


class DoctorProfilePublicAPIView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")
        return DoctorInfo.objects.filter(username=username)

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class DoctorProfileAPIView(CustomRetrieveAPIView):
    permission_classes = [IsAuthenticated, OwnProfilePermission, DoctorPermission]
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        return DoctorInfo.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorProfileDetailsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorProfileDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorEducationExperienceSettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorExperienceEducationSerializer

    def get_queryset(self):
        return DoctorInfo.objects.all()

    def get_object(self) -> DoctorInfo:
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorAvailableHoursSettingsAPIView(CustomListUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorAvailableHoursSerializerWithID

    @extend_schema(
        responses=DoctorAvailableHoursSerializerWithID(many=True),
        request=DoctorAvailableHoursSerializerWithID(many=True),
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        responses=DoctorAvailableHoursSerializerWithID(many=True),
        request=DoctorAvailableHoursSerializerWithID(many=True),
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        responses=DoctorAvailableHoursSerializerWithID(many=True),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        doctor_info = get_object_or_404(DoctorInfo, user=self.request.user)
        self.check_object_permissions(self.request, doctor_info)
        return doctor_info.doctoravailablehours_set.all()

    def perform_update(self, serializer):
        serializer.validated_data["doctor_info"] = self.request.user.doctor_info
        serializer.update(serializer.instance, serializer.validated_data)


class DoctorSpecialtySettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorSpecialtySettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorAccountSettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorAccountSettingsSerializer
    queryset = DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorProfessionalProfileAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorProfessionalProfileSerializer
    queryset = DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorReviewListCreateAPIView(CustomListCreateAPIView):
    serializer_class = DoctorReviewSerializer
    filterset_fields = ["created_at__gte", "created_at__lte"]

    @permission_classes([AllowAny])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        doctor_username = self.kwargs.get("username")
        doctor_info = get_object_or_404(DoctorInfo, username=doctor_username)
        return doctor_info.doctorreview_set.all()

    def perform_create(self, serializer):
        doctor_username = self.kwargs.get("username")
        serializer.validated_data["doctor_info"] = get_object_or_404(
            DoctorInfo, username=doctor_username
        )
        serializer.create(serializer.validated_data)
