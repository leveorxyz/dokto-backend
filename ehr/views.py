from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from django.conf import settings
import json
import re
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiExample,
    extend_schema,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes

from core.views import (
    CustomCreateAPIView,
    CustomListAPIView,
    CustomListCreateAPIView,
    CustomRetrieveAPIView,
    CustomRetrieveUpdateDestroyAPIView,
    CustomAPIView,
)
from ehr.models import (
    ChiefComplaintsAndHPI,
    ICDs,
    Orders,
    PatientProcedure,
    PhysicalExam,
    PlanOfCare,
    PatientEncounters,
    AssessmentDiagnosis,
    PatientSocialHistory,
    FunctionalAndCognitiveStatus,
    ReviewOfSystem,
    Vitals,
)
from .serializers import (
    AssessmentDiagnosisSerializer,
    ChiefComplaintsAndHPISerializer,
    OrdersSerializer,
    PatientProcedureSerializer,
    PhysicalExamSerializer,
    PlanOfCareSerializer,
    PatientEncounterSerializer,
    PatientEncounterViewSerializer,
    PatientSocialHistorySerializer,
    ICDSerializer,
    FunctionalAndCognitiveStatusSerializer,
    ReviewOfSystemSerializer,
    VitalsSerializer,
)

# Create your views here.


class AllEncounters(CustomListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    """
        Patient encounter endpoint

        Request method: POST

        Request fields
        ---
        - patient: uuid
        - provider: uuid
        - visit_date: string
        - location: string
        - reason: string
        - signed: boolean
    """
    # queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterViewSerializer

    def get_queryset(self):
        patient_uuid = self.kwargs["patient_uuid"]
        return PatientEncounters.objects.filter(patient_id=patient_uuid)


class AddEncounters(CustomCreateAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
    """
        Patient encounter endpoint

        Request method: POST

        Request fields
        ---
        - patient: uuid
        - provider: uuid
        - visit_date: string
        - location: string
        - reason: string
        - signed: boolean
    """
    queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterSerializer


class PatientEncountersView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterSerializer


class AssessmentDiagnosisByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]

    # queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return AssessmentDiagnosis.objects.filter(
            patient_encounter_id=patient_encounter_uuid
        )


class AssessmentDiagnosisView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient assesment and diagnosis endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
    """
    queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer


class AssessmentDiagnosisUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer


class PlanOfCareByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter medical notes endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
    """
    serializer_class = PlanOfCareSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return PlanOfCare.objects.filter(patient_encounter_id=patient_encounter_uuid)


class PlanOfCareView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter medical notes endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
    """
    queryset = PlanOfCare.objects.all()
    serializer_class = PlanOfCareSerializer


class PlanOfCareUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PlanOfCare.objects.all()
    serializer_class = PlanOfCareSerializer


class PatientSocialHistoryByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient social history endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
    """
    # queryset = PatientSocialHistory.objects.all()
    serializer_class = PatientSocialHistorySerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return PatientSocialHistory.objects.filter(
            patient_encounter_id=patient_encounter_uuid
        )


class PatientSocialHistoryView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient social history endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
    """
    queryset = PatientSocialHistory.objects.all()
    serializer_class = PatientSocialHistorySerializer


class PatientSocialHistoryUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PatientSocialHistory.objects.all()
    serializer_class = PatientSocialHistorySerializer


class ICDsView(CustomAPIView):
    http_method_names = ["get", "options"]
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[
                            {
                                "id": 0,
                                "code_description": "string",
                                "icd_code": "string",
                                "full_description": "string",
                            }
                        ],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, request, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "ehr_icds.json"))
        selected_rows = []
        for row in data:
            if re.search(
                kwargs["icd_description"], row["full_description"], re.IGNORECASE
            ):
                selected_rows.append(row)
        return super().get(request, response_data=selected_rows, *args, **kwargs)


class FunctionalAndCognitiveStatusByEncounterIdView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter Functional & Cognitive Status endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid


    """
    # queryset = FunctionalAndCognitiveStatus.objects.all()
    serializer_class = FunctionalAndCognitiveStatusSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return FunctionalAndCognitiveStatus.objects.filter(
            patient_encounter_id=patient_encounter_uuid
        )


class FunctionalAndCognitiveStatusView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter Functional & Cognitive Status endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid


    """
    queryset = FunctionalAndCognitiveStatus.objects.all()
    serializer_class = FunctionalAndCognitiveStatusSerializer


class FunctionalAndCognitiveStatusUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = FunctionalAndCognitiveStatus.objects.all()
    serializer_class = FunctionalAndCognitiveStatusSerializer


class ChiefComplaintsAndHPIByEncounterIDView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    """
        Chief Complaints And HPI endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid


    """
    serializer_class = ChiefComplaintsAndHPISerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return ChiefComplaintsAndHPI.objects.filter(
            patient_encounter_id=patient_encounter_uuid
        )

    def get_object(self):
        main_query = self.get_queryset()
        if len(main_query) != 0:
            return main_query.order_by("-created_at").first()
        raise get_object_or_404(main_query)


class ChiefComplaintsAndHPIView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Chief Complaints And HPI endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid


    """
    queryset = ChiefComplaintsAndHPI.objects.all()
    serializer_class = ChiefComplaintsAndHPISerializer


class ChiefComplaintsAndHPIUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ChiefComplaintsAndHPI.objects.all()
    serializer_class = ChiefComplaintsAndHPISerializer


class PatientProcedureByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient Procedure endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid


    """
    serializer_class = PatientProcedureSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return PatientProcedure.objects.filter(
            patient_encounter_id=patient_encounter_uuid
        )


class PatientProcedureView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient Procedure endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid

    """
    queryset = PatientProcedure.objects.all()
    serializer_class = PatientProcedureSerializer


class PatientProcedureUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PatientProcedure.objects.all()
    serializer_class = PatientProcedureSerializer


class ReviewOfSystemByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient ReviewOfSystem endpoint

        Request method: GET

        Request fields
        ---
        - patient_encounter: uuid

    """
    serializer_class = PatientProcedureSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return ReviewOfSystem.objects.filter(
            patient_encounter_id=patient_encounter_uuid
        )


class ReviewOfSystemView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient ReviewOfSystem endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid

    """
    queryset = ReviewOfSystem.objects.all()
    serializer_class = ReviewOfSystemSerializer


class ReviewOfSystemUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ReviewOfSystem.objects.all()
    serializer_class = ReviewOfSystemSerializer


class PhysicalExamByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient PhysicalExam endpoint

        Request method: GET

        Request fields
        ---
        - patient_encounter: uuid

    """
    serializer_class = PatientProcedureSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return PhysicalExam.objects.filter(patient_encounter_id=patient_encounter_uuid)


class PhysicalExamView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient PhysicalExam endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid

    """
    queryset = PhysicalExam.objects.all()
    serializer_class = PhysicalExamSerializer


class PhysicalExamUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PhysicalExam.objects.all()
    serializer_class = PhysicalExamSerializer


class OrdersByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient Orders endpoint

        Request method: GET

        Request fields
        ---
        - patient_encounter: uuid

    """
    serializer_class = PatientProcedureSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return Orders.objects.filter(patient_encounter_id=patient_encounter_uuid)


class OrdersView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient Orders endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid

    """
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrdersUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class VitalsByEncounterIDView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient Vitals endpoint

        Request method: GET

        Request fields
        ---
        - patient_encounter: uuid

    """
    serializer_class = VitalsSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs["patient_encounter_uuid"]
        return Vitals.objects.filter(patient_encounter_id=patient_encounter_uuid)


class VitalsView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient Vitals endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid


    """
    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer


class VitalsUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer
