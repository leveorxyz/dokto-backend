from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate, logout

from core.views import CustomRetrieveAPIView, CustomCreateAPIView
from core.utils import set_user_ip
from .models import User, DoctorInfo, PharmacyInfo, ClinicInfo
from .serializers import (
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


class LogoutView(APIView):
    def post(self, request):
        # Flushing current request session
        set_user_ip(request)
        logout(request)
        return Response(
            {
                "status_code": 200,
                "message": "Logout successful.",
                "result": None,
            }
        )


class UsernameExists(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_type=None, username=None):
        if not user_type or not username:
            raise ValidationError("Invalid request parameters.")

        # Checking if username exists
        user_model = {
            "doctor": DoctorInfo,
            "pharmacy": PharmacyInfo,
            "clinic": ClinicInfo,
        }

        try:
            if user_model[user_type].objects.filter(username=username).exists():
                return Response(
                    {
                        "status_code": 200,
                        "message": "Exists.",
                        "result": None,
                    }
                )
        except KeyError:
            raise ValidationError("Invalid user type.")

        return Response(
            {
                "status_code": 404,
                "message": "Does not exist.",
                "result": None,
            },
            status=HTTP_404_NOT_FOUND,
        )


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
