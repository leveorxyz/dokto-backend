from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout

from core.views import (
    CustomListAPIView,
    CustomRetrieveAPIView,
    CustomCreateAPIView,
    CustomAPIView,
)
from core.utils import set_user_ip
from .models import User, DoctorInfo
from .serializers import (
    DoctorDirectorySerializer,
    UserSerializer,
    UserLoginSerializer,
    VerifyEmailSerializer,
    DoctorRegistrationSerializer,
    ClinicRegistrationSerializer,
    PharmacyRegistrationSerializer,
    PatientRegistrationSerializer,
)


class UserRetrieveAPIView(CustomRetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        # Extracting data from request and validating it
        user = None
        fields = ["email", "password"]
        for field in fields:
            if field not in request.data:
                raise ValidationError(f"{field} is required")
        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")
        serializer = UserLoginSerializer(user)

        # Checking if user is already logged in
        result = None
        if request.user.is_authenticated:
            set_user_ip(request)
            result = UserLoginSerializer(request.user).data

        # Authenticating user
        else:
            user = authenticate(
                email=request.data["email"],
                password=request.data["password"],
            )
            if not user:
                raise AuthenticationFailed()
            result = serializer.data

        # Returning token
        return Response(
            {
                "status_code": 200,
                "message": "Login successful.",
                "result": result,
            }
        )


class LogoutView(CustomAPIView):
    http_method_names = ["post", "options"]

    def post(self, request):
        # Flushing current request session
        logout(request)
        return super().post(request=request)


class DoctorSignupView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.DOCTOR)
    serializer_class = DoctorRegistrationSerializer


class PatientSignupView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.PATIENT)
    serializer_class = PatientRegistrationSerializer


class ClinicSignupView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.CLINIC)
    serializer_class = ClinicRegistrationSerializer


class PharmacySignupView(CustomCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.PHARMACY)
    serializer_class = PharmacyRegistrationSerializer


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data={"token": kwargs["token"]})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        return Response(
            {
                "status_code": 200,
                "message": "Email verified successfully.",
                "result": UserLoginSerializer(instance=validated_data["user"]).data,
            }
        )


class DoctorsListView(CustomListAPIView):
    permission_classes = [AllowAny]
    queryset = DoctorInfo.objects.all()
    serializer_class = DoctorDirectorySerializer
