from rest_framework.permissions import IsAuthenticated

from core.views import CustomListAPIView, CustomListCreateAPIView
from core.permissions import DoctorPermission
from .models import Appointment
from .serializers import AppointmentSerializer

# Create your views here.
class AppointmentListCreateAPIView(CustomListCreateAPIView):
    """
    Appointment list create API view
    """

    permission_classes = (IsAuthenticated,)
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class EncounteredPatientListAPIView(CustomListAPIView):
    """
    List of encountered patients
    """

    permission_classes = [IsAuthenticated, DoctorPermission]
