from django.urls import path
from .views import (
    AllEncounters,
    AssessmentDiagnosisUpdateView,
    AssessmentDiagnosisView,
    MedicalNotesUpdateView,
    MedicalNotesView,
    PatientEncounters,
)

urlpatterns = [
    path("encounters/", AllEncounters.as_view(), name="encounter-list"),
    path(
        "patient-encounters/<uuid:pk>/",
        PatientEncounters.as_view(),
        name="patient-encounter-list",
    ),
    path(
        "encounters/assessments/",
        AssessmentDiagnosisView.as_view(),
        name="patient-encounter-assessments",
    ),
    path(
        "encounters/medical-notes/",
        MedicalNotesView.as_view(),
        name="patient-encounter-medical-notes",
    ),
    path(
        "encounters/assessments/<uuid:pk>/",
        AssessmentDiagnosisUpdateView.as_view(),
        name="patient-encounter-assessments-update",
    ),
    path(
        "encounters/medical-notes/<uuid:pk>/",
        MedicalNotesUpdateView.as_view(),
        name="patient-encounter-medical-notes-update",
    ),
]
