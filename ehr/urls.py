from django.urls import path
from .views import (
    AddEncounters,
    AllEncounters,
    AssessmentDiagnosisUpdateView,
    AssessmentDiagnosisView,
    AssessmentDiagnosisByEncounterIDView,
    ChiefComplaintsAndHPIByEncounterIDView,
    ChiefComplaintsAndHPIUpdateView,
    ChiefComplaintsAndHPIView,
    FunctionalAndCognitiveStatusByEncounterIdView,
    FunctionalAndCognitiveStatusUpdateView,
    FunctionalAndCognitiveStatusView,
    ICDsView,
    PatientProcedureByEncounterIDView,
    PatientProcedureUpdateView,
    PatientProcedureView,
    PlanOfCareUpdateView,
    PlanOfCareView,
    PlanOfCareByEncounterIDView,
    PatientEncountersView,
    PatientSocialHistoryUpdateView,
    PatientSocialHistoryView,
    PatientSocialHistoryByEncounterIDView,
)

urlpatterns = [
    path(
        "encounters/<uuid:patient_uuid>/",
        AllEncounters.as_view(),
        name="patient-encounter-list",
    ),
    path("encounters/add", AddEncounters.as_view(), name="encounter-add"),
    path(
        "patient-encounters/<uuid:pk>/",
        PatientEncountersView.as_view(),
        name="patient-encounter-list",
    ),
    path(
        "encounters/assessments/<uuid:patient_encounter_uuid>/",
        AssessmentDiagnosisByEncounterIDView.as_view(),
        name="patient-encounter-assessments",
    ),
    path(
        "encounters/assessments/",
        AssessmentDiagnosisView.as_view(),
        name="patient-encounter-assessments",
    ),
    path(
        "encounters/plan-of-care/",
        PlanOfCareView.as_view(),
        name="patient-encounter-plan-of-care",
    ),
    path(
        "encounters/plan-of-care/<uuid:patient_encounter_uuid>/",
        PlanOfCareByEncounterIDView.as_view(),
        name="patient-encounter-plan-of-care",
    ),
    path(
        "encounters/assessments/<uuid:pk>/",
        AssessmentDiagnosisUpdateView.as_view(),
        name="patient-encounter-assessments-update",
    ),
    path(
        "encounters/plan-of-care/<uuid:pk>/",
        PlanOfCareUpdateView.as_view(),
        name="patient-encounter-plan-of-care-update",
    ),
    path(
        "encounters/social-history/",
        PatientSocialHistoryView.as_view(),
        name="patient-social-history",
    ),
    path(
        "encounters/social-history/<uuid:patient_encounter_uuid>/",
        PatientSocialHistoryByEncounterIDView.as_view(),
        name="patient-social-history",
    ),
    path(
        "encounters/social-history/<uuid:pk>/",
        PatientSocialHistoryUpdateView.as_view(),
        name="patient-social-history-update",
    ),
    path(
        "encounters/icd/<str:icd_description>/",
        ICDsView.as_view(),
        name="icd-code-list",
    ),
    path(
        "encounters/functional-and-cognitive-status/",
        FunctionalAndCognitiveStatusView.as_view(),
        name="patient-functional-and-cognitive-status",
    ),
    path(
        "encounters/functional-and-cognitive-status-update/<uuid:pk>/",
        FunctionalAndCognitiveStatusUpdateView.as_view(),
        name="patient-functional-and-cognitive-status-update",
    ),
    path(
        "encounters/functional-and-cognitive-status/<uuid:patient_encounter_uuid>/",
        FunctionalAndCognitiveStatusByEncounterIdView.as_view(),
        name="patient-functional-and-cognitive-status",
    ),
    path(
        "encounters/chief-complaints-hpi/",
        ChiefComplaintsAndHPIView.as_view(),
        name="patient-chief-complaints-hpi",
    ),
    path(
        "encounters/chief-complaints-hpi-update/<uuid:pk>/",
        ChiefComplaintsAndHPIUpdateView.as_view(),
        name="patient-chief-complaints-hpi-update",
    ),
    path(
        "encounters/chief-complaints-hpi/<uuid:patient_encounter_uuid>/",
        ChiefComplaintsAndHPIByEncounterIDView.as_view(),
        name="patient-chief-complaints-hpi",
    ),
    path(
        "encounters/patient-procedure/",
        PatientProcedureView.as_view(),
        name="patient-patient-procedure",
    ),
    path(
        "encounters/patient-procedure/<uuid:patient_encounter_uuid>/",
        PatientProcedureByEncounterIDView.as_view(),
        name="patient-patient-procedure",
    ),
    path(
        "encounters/patient-procedure-update/<uuid:pk>/",
        PatientProcedureUpdateView.as_view(),
        name="patient-patient-procedure-update",
    ),
]
