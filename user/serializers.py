from typing import Union, List, Dict
from rest_framework.fields import SerializerMethodField

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    DateField,
    ListField,
    IntegerField,
    URLField,
    ChoiceField,
    EmailField,
)
from rest_framework.exceptions import ValidationError
from cryptography.fernet import InvalidToken
from core.models import CoreModel

from core.classes import ExpiringActivationTokenGenerator
from dashboard.models import HospitalTeam
from .models import (
    DoctorAvailableHours,
    DoctorEducation,
    DoctorProfession,
    DoctorReview,
    DoctorAcceptedInsurance,
    User,
    DoctorInfo,
    DoctorExperience,
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
        fields = ("patient_name", "star_count", "comment", "created_at")


class DoctorRegistrationSerializer(ModelSerializer):
    username = CharField(read_only=True, source="get_username")
    profile_photo = CharField(required=True)
    language = ListField(child=CharField(), write_only=True)
    education = ListField(child=DoctorEducationSerializer(), write_only=True)
    experience = ListField(
        child=DoctorExpericenceSerializer(), required=False, write_only=True
    )
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
    professional_bio = CharField(required=True, write_only=True)
    gender = ChoiceField(
        choices=PatientInfo.Gender.choices, required=True, write_only=True
    )
    date_of_birth = DateField(required=True, write_only=True)
    accepted_insurance = ListField(child=CharField(), required=False, write_only=True)
    accept_all_insurance = ListField(child=CharField(), write_only=True, required=False)
    license_expiration = DateField(required=True, write_only=True)
    profession = ListField(child=CharField(), write_only=True, required=False)
    affiliated_hospital_id = CharField(required=False, write_only=True)

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

    def validate(self, attrs):
        if "accepted_insurance" not in attrs and (
            "accept_all_insurance" not in attrs
            or len(attrs["accept_all_insurance"]) == 0
        ):
            raise ValidationError("You must accept at least one insurance")
        return super().validate(attrs)

    def create(self, validated_data: dict):
        # Check if doctor is affiliated to a hospital
        affiliated_hospital = None
        if "affiliated_hospital_id" in validated_data:
            affiliated_hospital = ClinicInfo.objects.get(
                user_id=validated_data.get("affiliated_hospital_id")
            )

        # Generate username
        username_suffix = (
            f" {affiliated_hospital.user.full_name}" if affiliated_hospital else ""
        )
        username = generate_username(
            DoctorInfo, validated_data.get("full_name") + username_suffix
        )

        validated_data.update({"user_type": User.UserType.DOCTOR})
        user: User = User.from_validated_data(validated_data=validated_data)
        user.save()
        try:
            user.profile_photo = validated_data.pop("profile_photo")
        except Exception as e:
            user.delete()
            raise e

        experience_data = []
        insurance_data = []
        profession_data = []
        if "experience" in validated_data:
            experience_data = validated_data.pop("experience")
        if "profession" in validated_data:
            profession_data = validated_data.pop("profession")
        if "accepted_insurance" in validated_data:
            insurance_data = validated_data.pop("accepted_insurance")
        else:
            insurance_data = ["all"]
        education_data = validated_data.pop("education")
        language = validated_data.pop("language")
        identification_photo = validated_data.pop("identification_photo")
        license_file = validated_data.pop("license_file")

        # Creating doctor info
        validated_data.update(
            {
                "user": user,
                "username": username,
                "affiliated_hospital": affiliated_hospital,
            }
        )
        try:
            doctor_info: DoctorInfo = DoctorInfo.from_validated_data(
                validated_data=validated_data
            )
            doctor_info.save()
            doctor_info.identification_photo = identification_photo
            doctor_info.license_file = license_file
            if affiliated_hospital:
                HospitalTeam.objects.create(
                    clinic=affiliated_hospital,
                    doctor=doctor_info,
                    profession=profession_data[0],
                )
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

        self.from_list(language, DoctorLanguage, "language", doctor_info=doctor_info)
        self.from_list(
            insurance_data,
            DoctorAcceptedInsurance,
            "insurance",
            doctor_info=doctor_info,
        )
        self.from_list(
            profession_data, DoctorProfession, "profession", doctor_info=doctor_info
        )

        try:
            user.send_email_verification_mail()
        except:
            pass
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
                "education",
                "experience",
                "accept_all_insurance",
                "profession",
                "affiliated_hospital_id",
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

        try:
            user.send_email_verification_mail()
        except:
            pass
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

        try:
            user.send_email_verification_mail()
        except:
            pass

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

        try:
            user.send_email_verification_mail()
        except:
            pass

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


class DoctorDirectorySerializer(ModelSerializer):
    full_name = CharField(source="user.full_name")
    email = CharField(source="user.email")
    street = CharField(source="user.street")
    state = CharField(source="user.state")
    city = CharField(source="user.city")
    zip_code = CharField(source="user.zip_code")
    country = CharField(source="user.country")
    contact_no = CharField(source="user.contact_no")

    class Meta:
        model = DoctorInfo
        main_fields = list(
            set(field.name for field in model._meta.fields)
            - set(model.get_hidden_fields() + ["user"])
        )
        extra_fields = list(
            set(field.name for field in User._meta.fields)
            - set(User.get_hidden_fields() + ["user_type", "password", "last_login"])
        )
        fields = main_fields + extra_fields
        extra_kwargs = {field: {"read_only": True} for field in extra_fields}


class FeaturedDoctorSerializer(ModelSerializer):
    full_name = CharField(source="user.full_name")
    profile_photo = CharField(source="user.profile_photo")
    address = SerializerMethodField()

    def get_address(self, obj):
        address_fields = ["street", "state", "city", "zip_code", "country"]
        return ", ".join(
            [
                getattr(obj.user, field)
                for field in address_fields
                if getattr(obj.user, field)
            ]
        )

    class Meta:
        model = DoctorInfo
        fields = [
            "full_name",
            "profile_photo",
            "username",
            "address",
            "rating",
            "review_count",
        ]
        extra_kwargs = {field: {"read_only": True} for field in fields}


class PasswordResetEmailSerializer(Serializer):
    email = EmailField(required=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise ValidationError("User does not exist")

        data["user"] = user
        return data


class PasswordResetSerializer(Serializer):
    password = CharField(required=True)
    token = CharField(required=True)
