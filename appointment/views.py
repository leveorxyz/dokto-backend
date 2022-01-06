from rest_framework.permissions import AllowAny

from core.views import CustomListAPIView, CustomListCreateAPIView
from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    EncounteredListSerializer,
)

# Create your views here.


class AppointmentListCreateAPIView(CustomListCreateAPIView):
    """
    Appointment list create API view
    """

    permission_classes = (AllowAny,)
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.all()



class EncounteredPatientListAPIView(CustomListAPIView):
    """
    List of encountered patients
    """

    permission_classes = [
        AllowAny,
    ]
    serializer_class = EncounteredListSerializer

    def get_queryset(self):
        return Appointment.objects.all()
