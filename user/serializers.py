import os

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)
from rest_framework.authtoken.models import Token
from django.conf import settings

from core.literals import PROFILE_PHOTO_DIRECTORY
from core.serializers import ReadWriteSerializerMethodField
from .models import User, DoctorInfo
from .utils import create_user, generate_image_file


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
    profile_photo = ReadWriteSerializerMethodField()

    def get_token(self, user: User):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_profile_photo(self, user: User):
        profile_photo = DoctorInfo.objects.filter(user=user).values_list(
            "profile_photo", flat=True
        )[0]
        return os.path.join(settings.MEDIA_URL, PROFILE_PHOTO_DIRECTORY, profile_photo)

    def create(self, validated_data):
        user = create_user(validated_data)

        # Exracting profile photo
        profile_photo = None
        if "profile_photo" in validated_data:
            profile_photo = generate_image_file(
                validated_data.pop("profile_photo"), user.id, PROFILE_PHOTO_DIRECTORY
            )

        # Creating doctor info
        DoctorInfo.objects.create(
            user=user, profile_photo=profile_photo, **validated_data
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
            "profile_photo",
        ]
