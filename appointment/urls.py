from django.urls import path

from . import views

urlpatterns = [
    path(
        "", views.AppointmentListCreateAPIView.as_view(), name="appointment-list-create"
    ),
    path(
        "encountered-patients/",
        views.EncounteredPatientListAPIView.as_view(),
        name="encountered-patients-list",
    ),
    path("doctors/", views.DoctorListAPIView.as_view(), name="doctor-list"),
]
