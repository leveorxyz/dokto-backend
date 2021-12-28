from django.urls import path

from .views import (
    ClinicLicenseAPIView,
    ClinicProfileAPIView,
    DoctorInsuranceAPIView,
    DoctorProfessionalProfileAPIView,
    DoctorProfileAPIView,
    DoctorProfileDetailsAPIView,
    DoctorProfilePublicAPIView,
    DoctorReviewListCreateAPIView,
    DoctorSpecialtySettingsAPIView,
    DoctorEducationExperienceSettingsAPIView,
    DoctorAvailableHoursSettingsAPIView,
    DoctorAccountSettingsAPIView,
    PatientProfileDetailsAPIView,
    AccountSettingsSerializer,
    PharmacyProfileAPIView,
)

urlpatterns = [
    path(
        "public/doctor/profile/<str:username>/",
        DoctorProfilePublicAPIView.as_view(),
        name="public-doctor-profile",
    ),
    path(
        "doctor/profile/",
        DoctorProfileAPIView.as_view(),
        name="doctor-profile",
    ),
    path(
        "doctor/profile-settings/profile-detail/",
        DoctorProfileDetailsAPIView.as_view(),
        name="doctor-profile-detail",
    ),
    path(
        "doctor/profile-settings/education-experience/",
        DoctorEducationExperienceSettingsAPIView.as_view(),
        name="doctor-education-experience",
    ),
    path(
        "doctor/profile-settings/available-hours/",
        DoctorAvailableHoursSettingsAPIView.as_view(),
        name="doctor-available-hours",
    ),
    path(
        "doctor/specialty-settings/",
        DoctorSpecialtySettingsAPIView.as_view(),
        name="doctor-specialty-settings",
    ),
    path(
        "doctor/account-settings/",
        DoctorAccountSettingsAPIView.as_view(),
        name="doctor-account-settings",
    ),
    path(
        "patient/profile-settings/",
        PatientProfileDetailsAPIView.as_view(),
        name="patient-profile-settings",
    ),
    path(
        "account-settings/",
        AccountSettingsSerializer.as_view(),
        name="account-settings",
    ),
    path(
        "doctor/professional-profile/",
        DoctorProfessionalProfileAPIView.as_view(),
        name="doctor-professional-profile",
    ),
    path(
        "doctor/review/<str:username>/",
        DoctorReviewListCreateAPIView.as_view(),
        name="doctor-review",
    ),
    path(
        "doctor/insurance/", DoctorInsuranceAPIView.as_view(), name="doctor-insurance"
    ),
    path(
        "clinic/profile-settings/",
        ClinicProfileAPIView.as_view(),
        name="clinic-profile-settings",
    ),
    path("clinic/license/", ClinicLicenseAPIView.as_view(), name="clinic-license"),
    path("pharmacy/profile-settings/", PharmacyProfileAPIView.as_view(),
         name="pharmacy-profile-settings"),
]
