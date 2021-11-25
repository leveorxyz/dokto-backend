from rest_framework.permissions import AllowAny

from core.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from ehr.models import MedicalNotes, PatientEncounters, AssessmentDiagnosis
from .serializers import (
    AssessmentDiagnosisSerializer,
    MedicalNotesSerializer,
    PatientEncounterSerializer,
)

# Create your views here.


class AllEncounters(CustomListCreateAPIView):
    permission_classes = [AllowAny]
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


class PatientEncounters(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterSerializer


class AssessmentDiagnosisView(CustomListCreateAPIView):
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


class MedicalNotesView(CustomListCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter medical notes endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
    """
    queryset = MedicalNotes.objects.all()
    serializer_class = MedicalNotesSerializer


class MedicalNotesUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = MedicalNotes.objects.all()
    serializer_class = MedicalNotesSerializer