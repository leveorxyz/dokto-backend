from django.urls import path

from .views import (
    DoctorProfessionalProfileAPIView,
    DoctorProfileAPIView,
    DoctorProfileDetailsAPIView,
    DoctorProfilePublicAPIView,
    DoctorSpecialtySettingsAPIView,
    DoctorEducationExperienceSettingsAPIView,
    DoctorAvailableHoursSettingsAPIView,
    DoctorAccountSettingsAPIView,
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
        "doctor/professional-profile/",
        DoctorProfessionalProfileAPIView.as_view(),
        name="doctor-professional-profile",
    ),
]
