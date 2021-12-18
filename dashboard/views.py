from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from drf_spectacular.utils import extend_schema
from core.serializers import AbstractAccountSettingsSerializer

from core.views import (
    CustomListCreateAPIView,
    CustomRetrieveAPIView,
    CustomRetrieveUpdateAPIView,
    CustomListUpdateAPIView,
)
from core.permissions import (
    OwnProfilePermission,
    DoctorPermission,
    PatientPermission,
)
from user.models import ClinicInfo, DoctorInfo, PatientInfo, PharmacyInfo
from user.serializers import DoctorReviewSerializer
from .serializers import (
    ClinicAccountSettingsSerializer,
    DoctorAcceptedInsuranceSerializer,
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorSpecialtySettingsSerializer,
    DoctorExperienceEducationSerializer,
    DoctorAvailableHoursSerializerWithID,
    DoctorAccountSettingsSerializer,
    PatientProfileDetailsSerializer,
    PatientAccountSettingsSerializer,
    DoctorProfessionalProfileSerializer,
    PharmacyAccountSettingsSerializer,
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


class PatientProfileDetailsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, PatientPermission, OwnProfilePermission]
    serializer_class = PatientProfileDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        return PatientInfo.objects.all()


class DoctorProfessionalProfileAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorProfessionalProfileSerializer
    queryset = DoctorInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class AccountSettingsSerializer(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, OwnProfilePermission]

    @extend_schema(
        responses=AbstractAccountSettingsSerializer,
        request=AbstractAccountSettingsSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses=AbstractAccountSettingsSerializer,
        request=AbstractAccountSettingsSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        responses=AbstractAccountSettingsSerializer,
        request=AbstractAccountSettingsSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        user_type = self.request.user.user_type
        user_type_model_map = {
            "DOCTOR": DoctorInfo,
            "PATIENT": PatientInfo,
            "CLINIC": ClinicInfo,
            "PHARMACY": PharmacyInfo,
        }
        if user_type not in user_type_model_map:
            raise ValidationError("Not implemented for this user")
        return user_type_model_map[user_type].objects.all()

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        user_type_model_map = {
            "DOCTOR": DoctorAccountSettingsSerializer,
            "PATIENT": PatientAccountSettingsSerializer,
            "CLINIC": ClinicAccountSettingsSerializer,
            "PHARMACY": PharmacyAccountSettingsSerializer,
        }
        if user_type not in user_type_model_map:
            raise ValidationError("Not implemented for this user")
        return user_type_model_map[user_type]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorReviewListCreateAPIView(CustomListCreateAPIView):
    serializer_class = DoctorReviewSerializer
    filterset_fields = ["created_at__gte", "created_at__lte"]
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class DoctorInsuranceAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = DoctorAcceptedInsuranceSerializer
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]

    def get_queryset(self):
        return DoctorInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)
