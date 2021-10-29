from django.urls import path

from .views import (
    DoctorProfileAPIView,
    DoctorProfileDetailsAPIView,
    DoctorSpecialtySettingsAPIView,
)

urlpatterns = [
    path(
        "doctor/<str:username>", DoctorProfileAPIView.as_view(), name="doctor-profile"
    ),
    path(
        "doctor/profile-settings/profile_detail/<str:username>",
        DoctorProfileDetailsAPIView.as_view(),
        name="doctor-profile-detail",
    ),
    path(
        "doctor/specialty-settings/<str:username>",
        DoctorSpecialtySettingsAPIView.as_view(),
        name="doctor-specialty-settings",
    ),
]
