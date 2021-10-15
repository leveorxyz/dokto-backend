from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from core.views import CustomRetrieveAPIView
from .models import User
from .serializers import UserSerializer, UserLoginSerializer


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
