from rest_framework.permissions import AllowAny

from core.views import (
    CustomCreateAPIView,
    CustomListAPIView,
    CustomListCreateAPIView,
    CustomRetrieveUpdateDestroyAPIView,
)
from ehr.models import (
    ChiefComplaintsAndHPI,
    ICDs,
    PatientProcedure,
    PlanOfCare,
    PatientEncounters,
    AssessmentDiagnosis,
    PatientSocialHistory,
    FunctionalAndCognitiveStatus
)
from .serializers import (
    AssessmentDiagnosisSerializer,
    ChiefComplaintsAndHPISerializer,
    PatientProcedureSerializer,
    PlanOfCareSerializer,
    PatientEncounterSerializer,
    PatientEncounterViewSerializer,
    PatientSocialHistorySerializer,
    ICDSerializer,
    FunctionalAndCognitiveStatusSerializer,
)

# Create your views here.

class AllEncounters(CustomListAPIView):
    permission_classes = [AllowAny]
    #permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]
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
    #queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterViewSerializer

    def get_queryset(self):
        patient_uuid = self.kwargs['patient_uuid']
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
    #permission_classes = [IsAuthenticated, DoctorPermission, OwnProfilePermission]

    #queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs['patient_encounter_uuid']
        return AssessmentDiagnosis.objects.filter(patient_encounter_id=patient_encounter_uuid)



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
    #queryset = PlanOfCare.objects.all()
    serializer_class = PlanOfCareSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs['patient_encounter_uuid']
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
    #queryset = PatientSocialHistory.objects.all()
    serializer_class = PatientSocialHistorySerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs['patient_encounter_uuid']
        return PatientSocialHistory.objects.filter(patient_encounter_id=patient_encounter_uuid)


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


class ICDsView(CustomListAPIView):
    permission_classes = [AllowAny]
   
    serializer_class = ICDSerializer

    def get_queryset(self):
        icd_description = self.kwargs['icd_description']
        return ICDs.objects.filter(full_description__contains=icd_description)



#############VIEW##########################
class FunctionalAndCognitiveStatusByEncounterIdView(CustomListAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter Functional & Cognitive Status endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
        

    """    
    #queryset = FunctionalAndCognitiveStatus.objects.all()
    serializer_class = FunctionalAndCognitiveStatusSerializer

    def get_queryset(self):
        patient_encounter_uuid = self.kwargs['patient_encounter_uuid']
        return FunctionalAndCognitiveStatus.objects.filter(patient_encounter_id=patient_encounter_uuid)



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


class  ChiefComplaintsAndHPIByEncounterIDView(CustomListAPIView):
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
        patient_encounter_uuid = self.kwargs['patient_encounter_uuid']
        return ChiefComplaintsAndHPI.objects.filter(patient_encounter_id=patient_encounter_uuid)


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


class  PatientProcedureByEncounterIDView(CustomListAPIView):
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
        patient_encounter_uuid = self.kwargs['patient_encounter_uuid']
        return PatientProcedure.objects.filter(patient_encounter_id=patient_encounter_uuid)


class PatientProcedureView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient Procedure endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
        

    """    
    queryset = ChiefComplaintsAndHPI.objects.all()
    serializer_class = PatientProcedureSerializer


class PatientProcedureUpdateView(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PatientProcedure.objects.all()
    serializer_class = PatientProcedureSerializer


