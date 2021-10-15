from django.urls import path

from .views import (
    UserRetrieveAPIView,
    LoginView,
    UsernameExists,
    LogoutView,
    DoctorSignupView,
)

urlpatterns = [
    path("<int:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
    path("doctor_signup/", DoctorSignupView.as_view(), name="doctor-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("exists/<str:username>", UsernameExists.as_view(), name="username-exists"),
]
