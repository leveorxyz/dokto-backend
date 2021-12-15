from rest_framework.exceptions import ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
)
from drf_spectacular.types import OpenApiTypes

from core.views import CustomAPIView
from core.permissions import ClinicPermission
from .serializers import OnboardSerializer


class OnboardMailAPIView(CustomAPIView):
    http_method_names = ["post", "options"]

    @extend_schema(
        request=OnboardSerializer,
    )
    @permission_classes((IsAuthenticated, ClinicPermission))
    def post(self, request, *args, **kwargs):
        if "doctor_id" not in request.data:
            raise ValidationError("doctor_id is required")
        self.request.user.clinic.send_onboard_mail(request.data["doctor_id"])
        return super().post(request, *args, **kwargs)
