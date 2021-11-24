from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ehr import views
from .views import (
    AllEncounters,
    AssessmentDiagnosisUpdateView,
    AssessmentDiagnosisView,
    MedicalNotesUpdateView,
    MedicalNotesView,
    PatientEncounters
)

urlpatterns = [
    #path("<uuid:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
 
    path('encounters/', AllEncounters.as_view(),name="encounter-list"),
    #path('encounters/', AllEncounters.as_view(), name="encounters"),
    #path('encounters/<int:pk>/', PatientEncounters.as_view()),
    path('patient-encounters/<uuid:pk>/', PatientEncounters.as_view(),name="patient-encounter-list"),

    path('encounters/assessments/', AssessmentDiagnosisView.as_view(),name="patient-encounter-assessments"),
    path('encounters/medical-notes/', MedicalNotesView.as_view(),name="patient-encounter-medical-notes"),
    
    path('encounters/assessments/<uuid:pk>/', AssessmentDiagnosisUpdateView.as_view(),name="patient-encounter-assessments-update"),
    path('encounters/medical-notes/<uuid:pk>/', MedicalNotesUpdateView.as_view(),name="patient-encounter-medical-notes-update"),

    #path('encounters/<uuid:pk>/', PatientEncounters.as_view(), name="patient-encounters"),
    
]
# urlpatterns = format_suffix_patterns(urlpatterns)

