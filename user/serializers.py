from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer:
    class Meta:
        model = User
        fields = ("id", "username", "email")
