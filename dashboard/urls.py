from django.urls import path

from .views import DoctorProfileAPIView

urlpatterns = [
    path(
        "doctor/<str:username>", DoctorProfileAPIView.as_view(), name="doctor-profile"
    ),
]
