from rest_framework.permissions import AllowAny

from core.views import CustomListAPIView, CustomListCreateAPIView
from .models import Appointment
from user.models import DoctorInfo
from .serializers import (
    AppointmentSerializer,
    EncounteredListSerializer,
    DummyDoctorListSerializer,
)

# Create your views here.
class AppointmentListCreateAPIView(CustomListCreateAPIView):
    """
    Appointment list create API view
    """

    permission_classes = (AllowAny,)
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class EncounteredPatientListAPIView(CustomListAPIView):
    """
    List of encountered patients
    """

    permission_classes = [
        AllowAny,
    ]
    queryset = Appointment.objects.all()
    serializer_class = EncounteredListSerializer


class DoctorListAPIView(CustomListAPIView):
    permission_classes = [AllowAny]
    queryset = DoctorInfo.objects.all()
    serializer_class = DummyDoctorListSerializer
