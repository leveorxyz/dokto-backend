from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

from .models import User


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
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
            full_name=validated_data["full_name"],
            street=validated_data["street"],
            state=validated_data["state"],
            city=validated_data["city"],
            zip_code=validated_data["zip_code"],
            contact_no=validated_data["contact_no"],
        )
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
