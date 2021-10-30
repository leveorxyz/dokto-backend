from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from core.views import CustomRetrieveAPIView
from user.models import User, DoctorInfo
from .serializers import DoctorProfileSerializer


class DoctorProfileAPIView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer
    queryset = User.objects.filter(user_type=User.UserType.DOCTOR)

    def get_queryset(self):
        username = self.kwargs.get("username")
        doctor = DoctorInfo.objects.get(username=username)
        return User.objects.filter(id=doctor.user_id)

    def get_object(self):
        return get_object_or_404(self.get_queryset())
