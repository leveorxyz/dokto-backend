from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from core.serializers import AbstractAccountSettingsSerializer

from core.views import (
    CustomAPIView,
    CustomListAPIView,
    CustomListCreateAPIView,
    CustomRetrieveAPIView,
    CustomRetrieveUpdateAPIView,
    CustomListUpdateAPIView,
)
from core.permissions import (
    ClinicPermission,
    OwnProfilePermission,
    DoctorPermission,
    PatientPermission,
    PharmacyPermission,
)
from user.models import ClinicInfo, DoctorInfo, PatientInfo, PharmacyInfo
from user.serializers import DoctorReviewSerializer
from .models import HospitalTeam, HospitalService
from .serializers import (
    ClinicAccountSettingsSerializer,
    ClinicProfileDetailsSerializer,
    ClinicLicenseSerializer,
    ClinicServiceListSerializer,
    ClinicTeamListSerializer,
    DoctorAcceptedInsuranceSerializer,
    DoctorInvoiceSerializer,
    DoctorProfileDetailsSerializer,
    DoctorProfileSerializer,
    DoctorExperienceEducationSerializer,
    DoctorAvailableHoursSerializerWithID,
    DoctorAccountSettingsSerializer,
    DoctorServiceSettingsSerializer,
    PatientProfileDetailsSerializer,
    PatientAccountSettingsSerializer,
    DoctorProfessionalProfileSerializer,
    PharmacyAccountSettingsSerializer,
    PharmacyAvailableHoursSettingsSerializer,
    PharmacyLicenseSerializer,
    PharmacyProfileDetailsSerializer,
    PharmacyProfileSettingsSerializer,
    PharmacyServicesSettingsSerializer,
)
from .filters import ReviewFilter


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
    queryset = PatientInfo.objects.all()

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


class DoctorServiceSettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    serializer_class = DoctorServiceSettingsSerializer
    queryset = DoctorInfo.objects.all()

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Successful",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value={
                            "services": {
                                "Cardiologist": [
                                    {
                                        "service": "string",
                                        "price": 0,
                                    }
                                ],
                                "Chiropractor": [
                                    {
                                        "service": "string",
                                        "price": 0,
                                    }
                                ],
                            }
                        },
                    )
                ],
                response=OpenApiTypes.ANY,
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Successful",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value={
                            "services": {
                                "Cardiologist": [
                                    {
                                        "service": "string",
                                        "price": 0,
                                    }
                                ],
                                "Chiropractor": [
                                    {
                                        "service": "string",
                                        "price": 0,
                                    }
                                ],
                            }
                        },
                    )
                ],
                response=OpenApiTypes.ANY,
            )
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Successful",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value={
                            "services": {
                                "Cardiologist": [
                                    {
                                        "service": "string",
                                        "price": 0,
                                    }
                                ],
                                "Chiropractor": [
                                    {
                                        "service": "string",
                                        "price": 0,
                                    }
                                ],
                            }
                        },
                    )
                ],
                response=OpenApiTypes.ANY,
            )
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

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
    filterset_class = ReviewFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="created_at__gte",
                type=OpenApiTypes.DATE,
                description="Filter review by creation time. Picks records greater than or equal to the input value. Format: YYYY-MM-DD",
            ),
            OpenApiParameter(
                name="created_at__lte",
                type=OpenApiTypes.DATE,
                description="Filter review by creation time. Picks records smaller than or equal to the input value. Format: YYYY-MM-DD",
            ),
        ],
        responses=DoctorReviewSerializer,
    )
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


class DoctorInsuranceAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = DoctorAcceptedInsuranceSerializer
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]

    def get_queryset(self):
        return DoctorInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)


class ClinicProfileAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = ClinicProfileDetailsSerializer
    permission_classes = [IsAuthenticated, ClinicPermission, OwnProfilePermission]

    def get_queryset(self):
        return ClinicInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)


class ClinicLicenseAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = ClinicLicenseSerializer
    permission_classes = [IsAuthenticated, ClinicPermission, OwnProfilePermission]

    def get_queryset(self):
        return ClinicInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)


class PharmacyProfileSettingsAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = PharmacyProfileSettingsSerializer
    permission_classes = [IsAuthenticated, PharmacyPermission, OwnProfilePermission]

    def get_queryset(self):
        return PharmacyInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class PharmacyLicenseAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = PharmacyLicenseSerializer
    permission_classes = [IsAuthenticated, PharmacyPermission, OwnProfilePermission]

    def get_queryset(self):
        return PharmacyInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class PharmacyProfileAPIView(CustomRetrieveAPIView):
    serializer_class = PharmacyProfileDetailsSerializer
    permission_classes = [IsAuthenticated, PharmacyPermission, OwnProfilePermission]

    def get_queryset(self):
        return PharmacyInfo.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class PharmacyProfilePublicAPIView(CustomRetrieveAPIView):
    serializer_class = PharmacyProfileDetailsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return PharmacyInfo.objects.all()

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(self.get_queryset(), username=username)


class PharmacyServiesSettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, PharmacyPermission, OwnProfilePermission]
    serializer_class = PharmacyServicesSettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return PharmacyInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class PharmacyAvailableHoursSettingsAPIView(CustomRetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, PharmacyPermission, OwnProfilePermission]
    serializer_class = PharmacyAvailableHoursSettingsSerializer

    def get_queryset(self, *args, **kwargs):
        return PharmacyInfo.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class ClinicTeamListAPIView(CustomListAPIView):
    permission_classes = [IsAuthenticated, ClinicPermission]
    serializer_class = ClinicTeamListSerializer

    def get_queryset(self, *args, **kwargs):
        return HospitalTeam.objects.filter(clinic=self.request.user.clinic_info)


class ClinicServiceListAPIView(CustomListAPIView):
    permission_classes = [IsAuthenticated, ClinicPermission]
    serializer_class = ClinicServiceListSerializer

    def get_queryset(self, *args, **kwargs):
        doctor_username = self.kwargs.get("doctor_username")
        return HospitalService.objects.filter(
            clinic=self.request.user.clinic_info, doctor__username=doctor_username
        )


class ClinicTeamRemoveAPIView(CustomAPIView):
    permission_classes = [IsAuthenticated, ClinicPermission]
    http_method_names = ["delete", "options"]

    def delete(self, request, *args, **kwargs):
        doctor_username = self.kwargs.get("doctor_username")
        HospitalService.objects.filter(
            clinic=self.request.user.clinic_info, doctor__username=doctor_username
        ).delete()
        HospitalTeam.objects.filter(
            clinic=self.request.user.clinic_info, doctor__username=doctor_username
        ).delete()
        return super().delete(request, response_data={}, *args, **kwargs)

class DoctorInvoiceAPIView(CustomRetrieveAPIView):
    serializer_class = DoctorInvoiceSerializer
    permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
