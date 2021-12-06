from rest_framework.permissions import AllowAny
from django.conf import settings
import json
import re

from core.views import (
    CustomCreateAPIView,
    CustomListAPIView,
    CustomRetrieveUpdateDestroyAPIView,
    CustomAPIView,
)
from ehr.models import (
    ICDs,
    PlanOfCare,
    PatientEncounters,
    AssessmentDiagnosis,
    PatientSocialHistory,
)
from .serializers import (
    AssessmentDiagnosisSerializer,
    PlanOfCareSerializer,
    PatientEncounterSerializer,
    PatientEncounterViewSerializer,
    PatientSocialHistorySerializer,
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
        - visit_reason: string
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
        - visit_reason: string
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

    def get(self, request, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "ehr_icds.json"))
        selected_rows = []
        for row in data:
            if re.search(
                kwargs["icd_description"], row["full_description"], re.IGNORECASE
            ):
                selected_rows.append(row)
        return super().get(request, response_data=selected_rows, *args, **kwargs)
