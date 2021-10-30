from django.urls import path

from .views import (
    UserRetrieveAPIView,
    LoginView,
    UsernameExists,
    LogoutView,
    DoctorSignupView,
    ClinicSignupView,
    PharmacySignupView,
    PatientSignupView,
)

urlpatterns = [
    path("<int:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
    path("doctor-signup/", DoctorSignupView.as_view(), name="doctor-signup"),
    path("clinic-signup/", ClinicSignupView.as_view(), name="clinic-signup"),
    path("pharmacy-signup/", PharmacySignupView.as_view(), name="pharmacy-signup"),
    path("patient-signup/", PatientSignupView.as_view(), name="patient-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "exists/<str:user_type>/<str:username>",
        UsernameExists.as_view(),
        name="username-exists",
    ),
]
