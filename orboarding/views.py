from rest_framework.exceptions import ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from core.views import CustomAPIView
from core.permissions import ClinicPermission

# Create your views here.


class OnboardMailAPIView(CustomAPIView):
    @permission_classes((IsAuthenticated, ClinicPermission))
    def post(self, request, *args, **kwargs):
        if "doctor_id" not in request.data:
            raise ValidationError("doctor_id is required")
        self.request.user.clinic.send_onboard_mail(request.data["doctor_id"])
        return super().post(request, *args, **kwargs)
