import os
import re

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ListField, JSONField, URLField

from core.serializers import ReadWriteSerializerMethodField
from .models import DoctorEducation, User, DoctorInfo, DoctorExperience, DoctorSpecialty
from .utils import create_user, generate_image_file_and_name


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
    country = CharField(write_only=True)
    gender = CharField(write_only=True)
    language = ListField(child=CharField(), write_only=True)
    education = ListField(child=JSONField(), write_only=True)
    professional_bio = CharField(write_only=True)
    linkedin_url = URLField(write_only=True, required=False)
    facebook_url = URLField(write_only=True, required=False)
    twitter_url = URLField(write_only=True, required=False)
    experience = ListField(child=JSONField(), write_only=True, required=False)
    specialty = ListField(child=CharField(), write_only=True)

    def get_token(self, user: User):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_profile_photo(self, user: User):
        return user.profile_photo.url

    def create(self, validated_data):
        user: User = create_user(validated_data, User.UserType.DOCTOR)

        # Extract education data
        education_data = validated_data.pop("education")

        # Extract experience data
        experience_data = []
        if "experience" in validated_data:
            experience_data = validated_data.pop("experience")

        # Extract specialty data
        specialty_data = validated_data.pop("specialty")

        # Creating doctor info
        doctor_info = DoctorInfo.objects.create(user=user, **validated_data)

        # Add doctor education
        for education in education_data:
            certificate = education.pop("certificate")
            doctor_edication = DoctorEducation.objects.create(
                **education, doctor_info=doctor_info
            )
            certificate_file_name, certificate_file = generate_image_file_and_name(
                certificate, user.id
            )
            doctor_edication.certificate.save(
                certificate_file_name, certificate_file, save=True
            )
            doctor_edication.save()

        # Add doctor experience
        DoctorExperience.objects.bulk_create(
            [
                DoctorExperience(**experience, doctor_info=doctor_info)
                for experience in experience_data
            ]
        )

        # Add doctor specialty
        DoctorSpecialty.objects.bulk_create(
            [
                DoctorSpecialty(specialty=specialty, doctor_info=doctor_info)
                for specialty in specialty_data
            ]
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
            "country",
            "gender",
            "language",
            "education",
            "professional_bio",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "experience",
            "specialty",
        ]
