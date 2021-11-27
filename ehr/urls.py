from django.urls import path
from .views import (
    AddEncounters,
    AllEncounters,
    AssessmentDiagnosisUpdateView,
    AssessmentDiagnosisView,
    MedicalNotesUpdateView,
    MedicalNotesView,
    PatientEncounters,
    PatientSocialHistoryUpdateView,
    PatientSocialHistoryView,
)

urlpatterns = [
    path("encounters/", AllEncounters.as_view(), name="encounter-list"),
    path("encounters/add", AddEncounters.as_view(), name="encounter-add"),
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
    path(
        "encounters/social-history/",
        PatientSocialHistoryView.as_view(),
        name="patient-social-history",
    ),
    path(
        "encounters/social-history/<uuid:pk>/",
        PatientSocialHistoryUpdateView.as_view(),
        name="patient-social-history-update",
    ),
]
