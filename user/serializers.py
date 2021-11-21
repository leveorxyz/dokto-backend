from django.db.models import fields
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
    DateField,
)
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ListField, IntegerField
from rest_framework.exceptions import ValidationError
from django.conf import settings
from cryptography.fernet import InvalidToken

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
    profile_photo = CharField(source="user.profile_photo")
    language = ListField(child=CharField(), write_only=True)
    education = ListField(child=DoctorEducationSerializer(), write_only=True)
    experience = ListField(
        child=DoctorExpericenceSerializer(), write_only=True, required=False
    )
    specialty = ListField(child=CharField(), write_only=True)
    identification_photo = CharField(source="identification_photo")
    license_file = CharField(source="license_file")
    accepted_insurance = ListField(child=CharField(), write_only=True, required=False)

    def create(self, validated_data):
        # Generate username
        username = generate_username(DoctorInfo, validated_data.get("full_name"))

        user: User = User.from_validated_data(
            validated_data=validated_data.update({"user_type": User.UserType.DOCTOR})
        )
        user.save()
        user.profile_photo = validated_data.pop("profile_photo")

        if "accepted_insurance" in validated_data:
            validated_data.pop("accepted_insurance")

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

        # Extract identification data
        identification_photo = validated_data.pop("identification_photo")

        # Extract license data
        license_file = validated_data.pop("license_file")

        # Creating doctor info
        try:
            doctor_info: DoctorInfo = DoctorInfo.from_validated_data(
                validated_data=validated_data.update(
                    {"user": user, "username": username}
                )
            )
            doctor_info.save()
            doctor_info.identification_photo = identification_photo
            doctor_info.license_file = license_file
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
            user.delete()
            raise e

        user.send_email_verification_mail()

        return user

    class Meta:
        model = User
        main_fields = [
            field.name
            for field in model._meta.fields
            if not field.name.startswith("_") and field.name != "password"
        ]
        extra_fields = [
            field.name
            for field in DoctorInfo._meta.fields
            if not field.name.startswith("_") and field.name not in ["id", "user"]
        ]
        fields = (
            main_fields + extra_fields + ["username", "token", "accepted_insurance"]
        )

        read_only_fields = ["token", "username"]
        write_only_fields = ["password"]
        required_false_fields = [
            "state",
            "city",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
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
