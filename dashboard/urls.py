from django.urls import path

from .views import (
    DoctorProfileAPIView,
    DoctorProfileDetailsAPIView,
    DoctorSpecialtySettingsAPIView,
    DoctorEducationExperienceSettingsAPIView,
)

urlpatterns = [
    path(
        "doctor/<str:username>", DoctorProfileAPIView.as_view(), name="doctor-profile"
    ),
    path(
        "doctor/profile-settings/profile-detail/<str:username>",
        DoctorProfileDetailsAPIView.as_view(),
        name="doctor-profile-detail",
    ),
    path(
        "doctor/profile-settings/education-experience/<str:username>",
        DoctorEducationExperienceSettingsAPIView.as_view(),
        name="doctor-education-experience",
    ),
    path(
        "doctor/specialty-settings/<str:username>",
        DoctorSpecialtySettingsAPIView.as_view(),
        name="doctor-specialty-settings",
    ),
]
