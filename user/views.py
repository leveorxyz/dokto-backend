from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate, logout

from core.views import CustomRetrieveAPIView, CustomCreateAPIView
from core.utils import set_user_ip
from .models import User
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    DoctorRegistrationSerializer,
    CollectiveRegistrationSerializer,
    PharmacyRegistrationSerializer,
)


class UserRetrieveAPIView(CustomRetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        User login endpoint

        Request method: POST

        Request fields
        ---
        - email: string
        - password: string

        Response codes
        ---
        - 200: User logged in successfully
        - 401: Invalid credentials

        Response fields
        ---
        - token: string
        - username: string
        - email: string
        """

        # Extracting data from request and validating it
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Checking if user is already logged in
        if request.user.is_authenticated:
            set_user_ip(request)
            return Response(
                {
                    "status_code": 200,
                    "message": "Login successful.",
                    "result": {
                        "username": request.user.get_username(),
                        "email": request.user.email,
                        "token": request.auth.key,
                    },
                }
            )

        # Authenticating user
        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user:
            raise AuthenticationFailed()

        # Returning token
        try:
            token, _ = Token.objects.get_or_create(user=user)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token expired.")
        else:
            return Response(
                {
                    "status_code": 200,
                    "message": "Login successful.",
                    "result": {
                        "username": user.get_username(),
                        "email": user.email,
                        "token": token.key,
                    },
                }
            )


class LogoutView(APIView):
    def post(self, request):
        """
        User logout endpoint

        Request method: POST

        Response codes
        ---
        - 200: User logged out successfully
        - 401: Invalid credentials
        """

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

    def get(self, request, username):
        """
        Check if username exists

        Request method: GET

        Response codes
        ---
        - 200: Username exists
        - 404: Username does not exist

        Response fields
        ---
        - status_code: int
        - message: string
        """

        # Checking if username exists
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "status_code": 200,
                    "message": "Username exists.",
                    "result": None,
                }
            )
        else:
            return Response(
                {
                    "status_code": 404,
                    "message": "Username does not exist.",
                    "result": None,
                },
                status=HTTP_404_NOT_FOUND,
            )


class DoctorSignupView(CustomCreateAPIView):
    """
    Doctor signup endpoint

    Request method: POST

    Request fields
    ---
    - username: string
    - email: string
    - password: string
    - full_name: string
    - contact_no: string
    - address:
        - street: string
        - city: string
        - state: string
        - zip_code: string
        - country: string
    """

    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.DOCTOR)
    serializer_class = DoctorRegistrationSerializer


class PatientSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Patient signup endpoint

        Request method: POST

        Request fields
        ---
        - username: string
        - email: string
        - password: string
        - first_name: string
        - last_name: string
        - phone_number: string
        - address:
            - street: string
            - city: string
            - state: string
            - zip_code: string
            - country: string
        """

        pass


class CollectiveSignupView(CustomCreateAPIView):
    """
    Collective signup endpoint

    Request method: POST

    Request fields
    ---
    - username: string
    - email: string
    - password: string
    - first_name: string
    - last_name: string
    - phone_number: string
    - address:
        - street: string
        - city: string
        - state: string
        - zip_code: string
        - country: string
    """

    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.COLLECTIVE)
    serializer_class = CollectiveRegistrationSerializer


class PharmacySignupView(CustomCreateAPIView):
    """
    Pharmacy signup endpoint

    Request method: POST

    Request fields
    ---
    - username: string
    - email: string
    - password: string
    - first_name: string
    - last_name: string
    - phone_number: string
    - address:
        - street: string
        - city: string
        - state: string
        - zip_code: string
        - country: string
    """

    permission_classes = [AllowAny]
    queryset = User.objects.filter(user_type=User.UserType.PHARMACY)
    serializer_class = PharmacyRegistrationSerializer