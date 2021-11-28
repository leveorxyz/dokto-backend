from typing import Union, List, Dict

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    DateField,
    ListField,
    IntegerField,
    URLField,
    ChoiceField,
)
from rest_framework.exceptions import ValidationError
from cryptography.fernet import InvalidToken
from core.models import CoreModel

from core.classes import ExpiringActivationTokenGenerator
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
from .utils import generate_username


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserLoginSerializer(ModelSerializer):
    username = CharField(source="get_username", read_only=True)

    class Meta:
        model = User
        fields = list(
            set(field.name for field in model._meta.fields) - set(["_profile_photo"])
        ) + ["token", "profile_photo", "username"]
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
    class Meta:
        model = DoctorEducation
        fields = fields = list(
            set(field.name for field in model._meta.fields)
            - set(model.get_hidden_fields())
        )
        extra_kwargs = {"doctor_info": {"required": False}}


class DoctorExpericenceSerializer(ModelSerializer):
    class Meta:
        model = DoctorExperience
        fields = list(
            set(field.name for field in model._meta.fields)
            - set(model.get_hidden_fields())
        )
        extra_kwargs = {"doctor_info": {"required": False}}


class DoctorSpecialtySerializer(ModelSerializer):
    class Meta:
        model = DoctorSpecialty
        fields = list(
            set(field.name for field in model._meta.fields)
            - set(model.get_hidden_fields())
        )
        extra_kwargs = {"doctor_info": {"required": False}}


class DoctorAvailableHoursSerializer(ModelSerializer):
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
    identification_type = ChoiceField(
        choices=DoctorInfo.IdentificationType.choices, required=True, write_only=True
    )
    identification_number = CharField(required=True, write_only=True)
    facebook_url = URLField(required=False, write_only=True)
    linkedin_url = URLField(required=False, write_only=True)
    twitter_url = URLField(required=False, write_only=True)
    license_file = CharField(required=True, write_only=True)
    awards = CharField(write_only=True, required=False)
    country = CharField(required=True, write_only=True)
    professional_bio = CharField(required=True, write_only=True)
    gender = ChoiceField(
        choices=PatientInfo.Gender.choices, required=True, write_only=True
    )
    date_of_birth = DateField(required=True, write_only=True)

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
        try:
            user.profile_photo = validated_data.pop("profile_photo")
        except Exception as e:
            user.delete()
            raise e

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
            "zip_code",
            "awards",
        ]
        extra_kwargs = {
            **{key: {"required": False} for key in required_false_fields},
            **{key: {"write_only": True} for key in write_only_fields},
            **{key: {"read_only": True} for key in read_only_fields},
        }


class PharmacyRegistrationSerializer(ModelSerializer):
    username = CharField(read_only=True, source="get_username")
    number_of_practitioners = IntegerField(
        required=False, source="pharmacy_info.number_of_practitioners"
    )
    profile_photo = CharField(required=True)

    def create(self, validated_data):
        # Generate username
        username = generate_username(PharmacyInfo, validated_data.get("full_name"))

        validated_data.update({"user_type": User.UserType.PHARMACY})
        user: User = User.from_validated_data(validated_data=validated_data)
        user.save()
        try:
            user.profile_photo = validated_data.pop("profile_photo")
        except Exception as e:
            user.delete()
            raise e

        # Extract pharmacy info
        pharmacy_data = {}
        if "pharmacy_data" in validated_data:
            pharmacy_data = validated_data.pop("pharmacy_data")
        try:
            pharmacy = PharmacyInfo.from_validated_data(
                validated_data={"user": user, "username": username, **pharmacy_data}
            )
            pharmacy.save()
        except Exception as e:
            user.delete()
            raise e

        return user

    class Meta:
        model = User
        main_fields = list(
            set(field.name for field in model._meta.fields)
            - set(User.get_hidden_fields() + ["user_type"])
        )
        extra_fields = list(
            set(field.name for field in PharmacyInfo._meta.fields)
            - set(PharmacyInfo.get_hidden_fields())
        )
        fields = (
            main_fields
            + extra_fields
            + [
                "username",
                "token",
                "profile_photo",
            ]
        )

        read_only_fields = ["token", "username", "last_login"]
        write_only_fields = ["password"]
        required_false_fields = ["state", "city", "zip_code", "number_of_practitioners"]
        extra_kwargs = {
            **{key: {"required": False} for key in required_false_fields},
            **{key: {"write_only": True} for key in write_only_fields},
            **{key: {"read_only": True} for key in read_only_fields},
        }


class ClinicRegistrationSerializer(PharmacyRegistrationSerializer):
    number_of_practitioners = IntegerField(
        required=False, source="clinic_info.number_of_practitioners"
    )

    def create(self, validated_data: dict):
        # Generate username
        username = generate_username(ClinicInfo, validated_data.get("full_name"))

        validated_data.update({"user_type": User.UserType.CLINIC})
        user: User = User.from_validated_data(validated_data=validated_data)
        user.save()

        try:
            user.profile_photo = validated_data.pop("profile_photo")
        except Exception as e:
            user.delete()
            raise e

        # Extract clinic info
        clinic_data = {}
        if "clinic_info" in validated_data:
            clinic_data = validated_data.pop("clinic_info")
        try:
            clinic = ClinicInfo.from_validated_data(
                validated_data={"user": user, "username": username, **clinic_data}
            )
            clinic.save()
        except Exception as e:
            user.delete()
            raise e

        return user


class PatientRegistrationSerializer(ModelSerializer):
    profile_photo = CharField(required=True)
    identification_photo = CharField(required=True, write_only=True)
    identification_type = ChoiceField(
        choices=PatientInfo.IdentificationType.choices, required=True, write_only=True
    )
    identification_number = CharField(required=True, write_only=True)
    referring_doctor_full_name = CharField(required=False, write_only=True)
    referring_doctor_phone_number = CharField(required=False, write_only=True)
    referring_doctor_address = CharField(required=False, write_only=True)
    insurance_type = ChoiceField(
        choices=PatientInfo.InsuranceType, required=False, write_only=True
    )
    insurance_name = CharField(required=False, write_only=True)
    insurance_number = CharField(required=False, write_only=True)
    insurance_policy_holder_name = CharField(required=False, write_only=True)
    date_of_birth = DateField(required=True, write_only=True)
    gender = ChoiceField(choices=PatientInfo.Gender.choices, write_only=True)
    name_of_parent = CharField(required=False, write_only=True)

    def create(self, validated_data):
        validated_data.update({"user_type": User.UserType.PATIENT})
        user: User = User.from_validated_data(
            validated_data=validated_data,
        )
        user.save()
        try:
            user.profile_photo = validated_data.pop("profile_photo")
        except Exception as e:
            user.delete()
            raise e

        identification_photo = validated_data.pop("identification_photo")
        validated_data.update({"user": user})
        try:
            patient_info = PatientInfo.from_validated_data(validated_data)
            patient_info.identification_photo = identification_photo
        except Exception as e:
            user.delete()
            raise e

        user.send_email_verification_mail()

        return user

    class Meta:
        model = User
        main_fields = list(
            set(field.name for field in model._meta.fields)
            - set(User.get_hidden_fields())
        )
        extra_fields = list(
            set(field.name for field in PatientInfo._meta.fields)
            - set(PatientInfo.get_hidden_fields())
        )
        fields = (
            main_fields
            + extra_fields
            + [
                "profile_photo",
                "identification_photo",
                "token",
            ]
        )

        read_only_fields = ["token", "last_login", "user_type"]
        write_only_fields = ["password"]
        required_false_fields = [
            "state",
            "city",
            "zip_code",
        ]
        extra_kwargs = {
            **{key: {"required": False} for key in required_false_fields},
            **{key: {"write_only": True} for key in write_only_fields},
            **{key: {"read_only": True} for key in read_only_fields},
        }


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

        user.is_active = True
        user.is_verified = True
        user.save()

        return data
