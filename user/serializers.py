from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ListField, URLField, IntegerField

from core.serializers import ReadWriteSerializerMethodField
from .models import (
    DoctorEducation,
    User,
    DoctorInfo,
    DoctorExperience,
    DoctorSpecialty,
    DoctorLanguage,
    CollectiveInfo,
    PharmacyInfo,
)
from .utils import create_user, generate_image_file_and_name


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserLoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True)


class DoctorEducationSerializer(ModelSerializer):
    certificate = CharField(required=True, write_only=True)

    def create(self, validated_data):
        certificate = validated_data.pop("certificate")
        doctor_info = validated_data.pop("doctor_info")
        doctor_education = DoctorEducation.objects.create(
            doctor_info=doctor_info, **validated_data
        )
        certificate_file_name, certificate_file = generate_image_file_and_name(
            certificate, doctor_info.id
        )
        doctor_education.certificate.save(
            certificate_file_name, certificate_file, save=True
        )
        doctor_education.save()
        return doctor_education

    class Meta:
        model = DoctorEducation
        fields = ["doctor_info", "course", "year", "college", "certificate"]


class DoctorExpericenceSerializer(ModelSerializer):
    class Meta:
        model = DoctorExperience
        fields = [
            "doctor_info",
            "establishment_name",
            "job_title",
            "start_date",
            "end_date",
            "job_description",
        ]


class DoctorSpecialtySerializer(ModelSerializer):
    class Meta:
        model = DoctorSpecialty
        fields = ["doctor_info", "specialty"]


class DoctorRegistrationSerializer(ModelSerializer):
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
    education = ListField(child=DoctorEducationSerializer(), write_only=True)
    professional_bio = CharField(write_only=True)
    linkedin_url = URLField(write_only=True, required=False)
    facebook_url = URLField(write_only=True, required=False)
    twitter_url = URLField(write_only=True, required=False)
    experience = ListField(
        child=DoctorEducationSerializer(), write_only=True, required=False
    )
    specialty = ListField(child=CharField(), write_only=True)

    def get_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_profile_photo(self, user: User) -> str:
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

        # Extract language data
        language = validated_data.pop("language")

        # Creating doctor info
        try:
            doctor_info = DoctorInfo.objects.create(user=user, **validated_data)
        except Exception as e:
            user.delete()
            raise e

        # Add doctor education
        try:
            for education in education_data:
                doctor_education_serializer = DoctorEducationSerializer(
                    data={"doctor_info": doctor_info.id, **education}
                )
                doctor_education_serializer.is_valid(raise_exception=True)
                doctor_education_serializer.save()
        except Exception as e:
            DoctorEducation.objects.filter(doctor_info=doctor_info).delete()
            doctor_info.delete()
            user.delete()
            raise e

        # Add doctor experience
        try:
            for experience in experience_data:
                doctor_experience_serializer = DoctorExpericenceSerializer(
                    data={"doctor_info": doctor_info.id, **experience}
                )
                doctor_experience_serializer.is_valid(raise_exception=True)
                doctor_experience_serializer.save()
        except Exception as e:
            DoctorExperience.objects.filter(doctor_info=doctor_info).delete()
            DoctorEducation.objects.filter(doctor_info=doctor_info).delete()
            doctor_info.delete()
            user.delete()
            raise e

        # Add doctor specialty
        try:
            for specialty in specialty_data:
                doctor_specialty_serializer = DoctorSpecialtySerializer(
                    data={"doctor_info": doctor_info.id, "specialty": specialty}
                )
                doctor_specialty_serializer.is_valid(raise_exception=True)
                doctor_specialty_serializer.save()
        except Exception as e:
            DoctorSpecialty.objects.filter(doctor_info=doctor_info).delete()
            DoctorExperience.objects.filter(doctor_info=doctor_info).delete()
            DoctorEducation.objects.filter(doctor_info=doctor_info).delete()
            doctor_info.delete()
            user.delete()
            raise e

        # Add doctor language
        try:
            if isinstance(language, str):
                language = [language]
            DoctorLanguage.objects.bulk_create(
                [
                    DoctorLanguage(doctor_info=doctor_info, language=lang)
                    for lang in language
                ]
            )
        except Exception as e:
            DoctorSpecialty.objects.filter(doctor_info=doctor_info).delete()
            DoctorExperience.objects.filter(doctor_info=doctor_info).delete()
            DoctorEducation.objects.filter(doctor_info=doctor_info).delete()
            DoctorLanguage.objects.filter(doctor_info=doctor_info).delete()
            doctor_info.delete()
            user.delete()
            raise e

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


class PharmacyRegistrationSerializer(ModelSerializer):
    token = SerializerMethodField()
    password = CharField(write_only=True)
    full_name = CharField(write_only=True)
    street = CharField(write_only=True)
    state = CharField(write_only=True)
    city = CharField(write_only=True)
    zip_code = CharField(write_only=True)
    contact_no = CharField(write_only=True)
    profile_photo = ReadWriteSerializerMethodField()
    number_of_practitioners = IntegerField(write_only=True)

    def get_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_profile_photo(self, user: User) -> str:
        return user.profile_photo.url

    def create(self, validated_data):
        user: User = create_user(validated_data, User.UserType.PHARMACY)

        # Extract pharmacy info
        try:
            PharmacyInfo.objects.create(user=user, **validated_data)
        except Exception as e:
            user.delete()
            raise e

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
            "number_of_practitioners",
        ]


class CollectiveRegistrationSerializer(PharmacyRegistrationSerializer):
    collective_type = CharField(write_only=True)

    def create(self, validated_data):
        user: User = create_user(validated_data, User.UserType.COLLECTIVE)

        # Extract collective info
        try:
            CollectiveInfo.objects.create(user=user, **validated_data)
        except Exception as e:
            user.delete()
            raise e

        return user

    class Meta:
        model = User
        fields = PharmacyRegistrationSerializer.Meta.fields + ["collective_type"]
