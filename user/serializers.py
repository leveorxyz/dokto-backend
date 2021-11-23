from typing import Union, List, Dict

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
    DateField,
    ListField,
    IntegerField,
    URLField,
)
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.conf import settings
from cryptography.fernet import InvalidToken
from stripe.api_resources import source
from core.models import CoreModel

from core.serializers import ReadWriteSerializerMethodField
from core.classes import ExpiringActivationTokenGenerator
from core.modelutils import send_mail
from .models import (
    DoctorAvailableHours,
    DoctorEducation,
    DoctorReview,
    User,
    DoctorInfo,
    DoctorExperience,
    DoctorSpecialty,
    DoctorLanguage,
    ClinicInfo,
    PharmacyInfo,
    PatientInfo,
)
from .utils import generate_username, generate_file_and_name


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [field.name for field in model._meta.fields] + ["token"]
        extra_kwargs = {field: {"read_only": True} for field in fields}
        extra_kwargs["password"] = {"write_only": True}
        del extra_kwargs["email"]


class DoctorInfoSerializer(ModelSerializer):
    model = DoctorInfo
    fields = [
        "id",
        "date_of_birth",
        "country",
        "gender",
        "professional_bio",
        "linkedin_url",
        "facebook_url",
        "twitter_url",
    ]


class DoctorEducationSerializer(ModelSerializer):
    certificate = CharField(required=True, write_only=True)

    def create(self, validated_data):
        certificate = validated_data.pop("certificate")
        doctor_info = validated_data.pop("doctor_info")
        doctor_education = DoctorEducation.objects.create(
            doctor_info=doctor_info, **validated_data
        )
        doctor_education.certificate = certificate
        return doctor_education

    class Meta:
        model = DoctorEducation
        fields = ["doctor_info", "course", "year", "college", "certificate"]
        extra_kwargs = {"doctor_info": {"required": False}}


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
        extra_kwargs = {"doctor_info": {"required": False}}


class DoctorSpecialtySerializer(ModelSerializer):
    class Meta:
        model = DoctorSpecialty
        fields = ["doctor_info", "specialty"]
        extra_kwargs = {"doctor_info": {"required": False}}


class DoctorAvailableHoursSerializer(ModelSerializer):
    day_of_week = SerializerMethodField()

    class Meta:
        model = User

    def get_day_of_week(self, instance):
        return instance.get_day_of_week_display()

    class Meta:
        model = DoctorAvailableHours
        fields = [
            "day_of_week",
            "start_time",
            "end_time",
        ]


class DoctorReviewSerializer(ModelSerializer):
    class Meta:
        model = DoctorReview
        fields = ("patient_name", "star_count", "comment")


class DoctorRegistrationSerializer(ModelSerializer):
    username = CharField(read_only=True, source="get_username")
    profile_photo = CharField(required=True)
    language = ListField(child=CharField(), write_only=True)
    education = ListField(child=DoctorEducationSerializer(), write_only=True)
    experience = ListField(
        child=DoctorExpericenceSerializer(), required=False, write_only=True
    )
    specialty = ListField(child=CharField(), write_only=True)
    accepted_insurance = ListField(child=CharField(), write_only=True, required=False)

    # Doctor fields
    identification_photo = CharField(required=True, write_only=True)
    identification_type = CharField(
        required=True, source="doctor_info.identification_type"
    )
    identification_number = CharField(
        required=True, source="doctor_info.identification_number"
    )
    facebook_url = URLField(required=False, source="doctor_info.facebook_url")
    linkedin_url = URLField(required=False, source="doctor_info.linkedin_url")
    twitter_url = URLField(required=False, source="doctor_info.twitter_url")
    license_file = CharField(required=True, write_only=True)
    awards = CharField(source="doctor_info.awards")
    country = CharField(required=True, source="doctor_info.country")
    professional_bio = CharField(required=True, source="doctor_info.professional_bio")
    gender = CharField(required=True, source="doctor_info.gender")
    date_of_birth = DateField(required=True, source="doctor_info.date_of_birth")

    def from_serializer(
        self, data: Union[List, Dict], serializer_class: ModelSerializer, **extra_info
    ) -> None:
        if not isinstance(data, list):
            data = [data]
        for item in data:
            serializer_instance = serializer_class(data={**item, **extra_info})
            serializer_instance.is_valid(raise_exception=True)
            serializer_instance.save()

    def from_list(
        self, data: List, model: CoreModel, keyword: str, **extra_info
    ) -> None:
        model.objects.bulk_create(
            [model(**{keyword: item, **extra_info}) for item in data]
        )

    def create(self, validated_data: dict):
        # Generate username
        username = generate_username(DoctorInfo, validated_data.get("full_name"))

        validated_data.update({"user_type": User.UserType.DOCTOR})
        user: User = User.from_validated_data(validated_data=validated_data)
        user.save()
        user.profile_photo = validated_data.pop("profile_photo")

        experience_data = []
        if "experience" in validated_data:
            experience_data = validated_data.pop("experience")
        if "accepted_insurance" in validated_data:
            validated_data.pop("accepted_insurance")
        education_data = validated_data.pop("education")
        specialty_data = validated_data.pop("specialty")
        language = validated_data.pop("language")
        identification_photo = validated_data.pop("identification_photo")
        license_file = validated_data.pop("license_file")

        # Creating doctor info
        validated_data.update({"user": user, "username": username})
        try:
            doctor_info: DoctorInfo = DoctorInfo.from_validated_data(
                validated_data=validated_data
            )
            doctor_info.save()
            doctor_info.identification_photo = identification_photo
            doctor_info.license_file = license_file
        except Exception as e:
            user.delete()
            raise e

        try:
            self.from_serializer(
                education_data, DoctorEducationSerializer, doctor_info=doctor_info.id
            )
        except Exception as e:
            user.delete()
            raise e
        try:
            self.from_serializer(
                experience_data, DoctorExpericenceSerializer, doctor_info=doctor_info.id
            )
        except Exception as e:
            user.delete()
            raise e

        self.from_list(
            specialty_data, DoctorSpecialty, "specialty", doctor_info=doctor_info
        )
        self.from_list(language, DoctorLanguage, "language", doctor_info=doctor_info)

        user.send_email_verification_mail()

        return user

    class Meta:
        model = User
        main_fields = list(
            set(field.name for field in model._meta.fields)
            - set(User.get_hidden_fields() + ["user_type"])
        )
        extra_fields = list(
            set(field.name for field in DoctorInfo._meta.fields)
            - set(DoctorInfo.get_hidden_fields())
        )
        fields = (
            main_fields
            + extra_fields
            + [
                "username",
                "token",
                "accepted_insurance",
                "license_file",
                "language",
                "profile_photo",
                "identification_photo",
                "specialty",
                "education",
                "experience",
            ]
        )

        read_only_fields = ["token", "username", "last_login"]
        write_only_fields = ["password"]
        required_false_fields = [
            "state",
            "city",
            "awards",
        ]
        extra_kwargs = {
            **{key: {"required": False} for key in required_false_fields},
            **{key: {"write_only": True} for key in write_only_fields},
            **{key: {"read_only": True} for key in read_only_fields},
        }


class PharmacyRegistrationSerializer(ModelSerializer):
    username = ReadWriteSerializerMethodField(required=True, allow_null=False)
    token = SerializerMethodField()
    password = CharField(write_only=True)
    full_name = CharField(write_only=True)
    street = CharField(write_only=True)
    state = CharField(write_only=True, required=False)
    city = CharField(write_only=True, required=False)
    zip_code = CharField(write_only=True)
    contact_no = CharField(write_only=True)
    profile_photo = ReadWriteSerializerMethodField()
    number_of_practitioners = IntegerField(write_only=True)

    def get_username(self, user: User) -> str:
        return PharmacyInfo.objects.get(user=user).username

    def get_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_profile_photo(self, user: User) -> str:
        return user.profile_photo.url

    def create(self, validated_data):
        # Generate username
        username = generate_username(DoctorInfo, validated_data.get("full_name"))

        user: User = User.from_validated_data(
            validated_data=validated_data.update({"user_type": User.UserType.PHARMACY})
        )
        user.save()
        user.profile_photo = validated_data.pop("profile_photo")

        # Extract pharmacy info
        try:
            PharmacyInfo.objects.create(user=user, username=username, **validated_data)
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


class ClinicRegistrationSerializer(PharmacyRegistrationSerializer):
    clinic_type = CharField(write_only=True)

    def get_username(self, user: User) -> str:
        return ClinicInfo.objects.get(user=user).username

    def create(self, validated_data):
        # Generate username
        username = generate_username(DoctorInfo, validated_data.get("full_name"))

        user: User = User.from_validated_data(
            validated_data=validated_data.update({"user_type": User.UserType.PHARMACY})
        )
        user.save()
        user.profile_photo = validated_data.pop("profile_photo")

        # Extract clinic info
        try:
            ClinicInfo.objects.create(user=user, username=username, **validated_data)
        except Exception as e:
            user.delete()
            raise e

        return user

    class Meta:
        model = User
        fields = PharmacyRegistrationSerializer.Meta.fields + ["clinic_type"]


class PatientRegistrationSerializer(ModelSerializer):
    token = SerializerMethodField()
    password = CharField(write_only=True)
    full_name = CharField(write_only=True)
    street = CharField(write_only=True)
    state = CharField(write_only=True, required=False)
    city = CharField(write_only=True, required=False)
    zip_code = CharField(write_only=True)
    contact_no = CharField(write_only=True)
    profile_photo = ReadWriteSerializerMethodField()
    date_of_birth = DateField(write_only=True)
    gender = CharField(write_only=True)
    social_security_number = CharField(write_only=True, required=False)
    identification_type = CharField(write_only=True)
    identification_number = CharField(write_only=True)
    identification_photo = CharField(write_only=True)

    # Insurance details
    insurance_type = CharField(write_only=True)
    insurance_name = CharField(write_only=True, required=False)
    insurance_number = CharField(write_only=True, required=False)
    insurance_policy_holder_name = CharField(write_only=True, required=False)

    # Insurance reference
    referring_doctor_full_name = CharField(write_only=True, required=False)
    referring_doctor_phone_number = CharField(write_only=True, required=False)
    referring_doctor_address = CharField(write_only=True, required=False)

    def get_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_profile_photo(self, user: User) -> str:
        return user.profile_photo.url

    def create(self, validated_data):
        host_url = self.context["request"].build_absolute_uri()
        user: User = User.from_validated_data(
            validated_data=validated_data.update({"user_type": User.UserType.PHARMACY})
        )
        user.save()
        user.profile_photo = validated_data.pop("profile_photo")

        # Extract identification data
        identification_photo = validated_data.pop("identification_photo")

        if "full_name" in validated_data:
            validated_data.pop("full_name")

        # Extract patient info
        try:
            patient_info = PatientInfo.objects.create(user=user, **validated_data)
            (
                identification_photo_name,
                identification_photo,
            ) = generate_file_and_name(identification_photo, patient_info.id)
            patient_info.identification_photo.save(
                identification_photo_name, identification_photo, save=True
            )
        except Exception as e:
            user.delete()
            raise e

        confirmation_token = ExpiringActivationTokenGenerator().generate_token(
            text=user.email
        )

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "email-verification",
                ]
            )
            + f"?token={confirmation_token.decode('utf-8')}"
        )

        send_mail(
            to_email=user.email,
            subject=f"Welcome to Dokto, please verify your email address",
            template_name="email/patient_verification.html",
            input_context={"name": user.full_name, "link": link, "host_url": host_url},
        )

        return user

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "token",
            "password",
            "full_name",
            "street",
            "state",
            "city",
            "zip_code",
            "contact_no",
            "profile_photo",
            "date_of_birth",
            "gender",
            "social_security_number",
            "identification_type",
            "identification_number",
            "identification_photo",
            "insurance_type",
            "insurance_name",
            "insurance_number",
            "insurance_policy_holder_name",
            "referring_doctor_full_name",
            "referring_doctor_phone_number",
            "referring_doctor_address",
        ]


class VerifyEmailSerializer(Serializer):
    token = CharField(required=True, write_only=True)

    def validate(self, data):
        try:
            email = ExpiringActivationTokenGenerator().get_token_value(data["token"])
        except InvalidToken:
            raise ValidationError("Invalid token")

        try:
            user = User.objects.get(email=email)
            data["user"] = user
        except User.DoesNotExist:
            raise ValidationError("User does not exist")

        if not user.is_active:
            user.is_active = True
            user.is_verified = True
            user.save()

        return data
