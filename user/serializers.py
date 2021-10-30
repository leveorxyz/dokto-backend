from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
    DateField,
)
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ListField, URLField, IntegerField

from core.serializers import ReadWriteSerializerMethodField
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
from .utils import create_user, generate_image_file_and_name


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserLoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True)


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
        child=DoctorExpericenceSerializer(), write_only=True, required=False
    )
    specialty = ListField(child=CharField(), write_only=True)
    identification_type = CharField(write_only=True)
    identification_photo = CharField(write_only=True)
    date_of_birth = DateField(write_only=True)

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

        # Extract identification data
        identification_photo = validated_data.pop("identification_photo")

        # Creating doctor info
        try:
            doctor_info: DoctorInfo = DoctorInfo.objects.create(
                user=user, **validated_data
            )
            (
                identification_photo_name,
                identification_photo,
            ) = generate_image_file_and_name(identification_photo, doctor_info.id)
            doctor_info.identification_photo.save(
                identification_photo_name, identification_photo, save=True
            )
            doctor_info.save()
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
            "identification_type",
            "identification_photo",
            "date_of_birth",
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


class ClinicRegistrationSerializer(PharmacyRegistrationSerializer):
    clinic_type = CharField(write_only=True)

    def create(self, validated_data):
        user: User = create_user(validated_data, User.UserType.CLINIC)

        # Extract clinic info
        try:
            ClinicInfo.objects.create(user=user, **validated_data)
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
    state = CharField(write_only=True)
    city = CharField(write_only=True)
    zip_code = CharField(write_only=True)
    contact_no = CharField(write_only=True)
    profile_photo = ReadWriteSerializerMethodField()
    date_of_birth = DateField(write_only=True)
    gender = CharField(write_only=True)
    social_security_number = CharField(write_only=True, required=False)
    identification_type = CharField(write_only=True)
    identification_number = CharField(write_only=True)

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
        user: User = create_user(validated_data, User.UserType.PATIENT)

        # Extract patient info
        try:
            PatientInfo.objects.create(user=user, **validated_data)
        except Exception as e:
            user.delete()
            raise e

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
            "insurance_type",
            "insurance_name",
            "insurance_number",
            "insurance_policy_holder_name",
            "referring_doctor_full_name",
            "referring_doctor_phone_number",
            "referring_doctor_address",
        ]
