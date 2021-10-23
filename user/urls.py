from django.urls import path

from .views import (
    UserRetrieveAPIView,
    LoginView,
    UsernameExists,
    LogoutView,
    DoctorSignupView,
    CollectiveSignupView,
    PharmacySignupView,
    PatientSignupView,
)

urlpatterns = [
    path("<int:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
    path("doctor_signup/", DoctorSignupView.as_view(), name="doctor-signup"),
    path(
        "collective_signup/", CollectiveSignupView.as_view(), name="collective-signup"
    ),
    path("pharmacy_signup/", PharmacySignupView.as_view(), name="pharmacy-signup"),
    path("patient_signup/", PatientSignupView.as_view(), name="patient-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("exists/<str:username>", UsernameExists.as_view(), name="username-exists"),
]
