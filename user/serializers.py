from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)
from rest_framework.authtoken.models import Token

from .models import User
from .utils import create_user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserLoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True)


class DoctorSerializer(ModelSerializer):
    token = SerializerMethodField()
    password = CharField(write_only=True)
    full_name = CharField(write_only=True)
    street = CharField(write_only=True)
    state = CharField(write_only=True)
    city = CharField(write_only=True)
    zip_code = CharField(write_only=True)
    contact_no = CharField(write_only=True)

    def get_token(self, user: User):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def create(self, validated_data):
        user = create_user(validated_data)
        return user

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "token",
            "full_name",
            "street",
            "state",
            "city",
            "zip_code",
            "contact_no",
        ]
