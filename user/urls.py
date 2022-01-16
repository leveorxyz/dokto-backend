from django.urls import path

from .views import (
    DoctorsListView,
    FeaturedDoctorListView,
    UserRetrieveAPIView,
    LoginView,
    LogoutView,
    DoctorSignupView,
    ClinicSignupView,
    PharmacySignupView,
    PatientSignupView,
    VerifyEmailView,
    PasswordResetEmailView,
    PasswordResetView,
)

urlpatterns = [
    path("<uuid:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
    path("doctor-signup/", DoctorSignupView.as_view(), name="doctor-signup"),
    path("clinic-signup/", ClinicSignupView.as_view(), name="clinic-signup"),
    path("pharmacy-signup/", PharmacySignupView.as_view(), name="pharmacy-signup"),
    path("patient-signup/", PatientSignupView.as_view(), name="patient-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activate/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("doctors/", DoctorsListView.as_view(), name="doctors-list"),
    path(
        "send-password-reset-email/",
        PasswordResetEmailView.as_view(),
        name="send-password-reset-email",
    ),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "featured-doctors/", FeaturedDoctorListView.as_view(), name="featured-doctors"
    ),
]
