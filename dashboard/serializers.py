from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    SerializerMethodField,
    CharField,
    EmailField,
    BooleanField,
)
from rest_framework.exceptions import ValidationError

from core.serializers import (
    ReadWriteSerializerMethodField,
    CustomCreateUpdateDeleteObjectOperationSerializer,
)
from user.models import (
    DoctorAvailableHours,
    DoctorInfo,
    DoctorSpecialty,
    DoctorEducation,
    DoctorExperience,
)
from user.serializers import (
    DoctorEducationSerializer,
    DoctorExpericenceSerializer,
    DoctorAvailableHoursSerializer,
    DoctorReviewSerializer,
)
from user.utils import generate_file_and_name


class DoctorProfileDetailsSerializer(ModelSerializer):
    """
    Serializes the `Dashboard > Profile Settings > Profile Details` page
    """

    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = CharField(
        source="user.profile_photo", required=False, allow_null=True
    )

    def update(self, instance: DoctorInfo, validated_data: dict) -> DoctorInfo:
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            instance.user.update_from_validated_data(user_data)
            if "profile_photo" in user_data:
                profile_photo_data = user_data.pop("profile_photo")
                instance.user.profile_photo = profile_photo_data

        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = DoctorInfo
        fields = [
            "full_name",
            "gender",
            "contact_no",
            "profile_photo",
            "professional_bio",
        ]


class DoctorEducationSerializerWithID(DoctorEducationSerializer):
    """
    Serializer for DoctorEducation model which includes `id` field in addition.
    This serializer will only be used for GET request of `dashboard > profile settings > experience and education`.
    PUT/PATCH requests will be handled by another serializer below.
    """

    def get_certificate(self, doctor_education: DoctorEducation):
        return doctor_education.certificate.url

    class Meta(DoctorEducationSerializer.Meta):
        fields = [
            "id",
            "doctor_info",
            "course",
            "year",
            "college",
        ]


class DoctorEducationUpdateSerializerWithID(ModelSerializer):
    """
    Serializer for DoctorEducation model which includes `id` and `operation` fields in addition.
    This serializer will only be used for PUT/PATCH request of
    `dashboard > profile settings > experience and education`.
    """

    operation = CharField(required=True, allow_null=False, write_only=True)

    def create(self, validated_data):
        validated_data.pop("operation")
        return super().create(validated_data)

    class Meta:
        model = DoctorEducation
        fields = [
            "id",
            "doctor_info",
            "course",
            "year",
            "college",
            "operation",
        ]
        extra_kwargs = {
            "id": {"read_only": False, "required": False},
            "doctor_info": {"required": False},
            "course": {"required": False},
            "year": {"required": False},
            "college": {"required": False},
        }


class DoctorExpericenceSerializerWithID(DoctorExpericenceSerializer):
    """
    Serializer for DoctorExpericence model which includes `id` field in addition.
    This serializer will only be used for GET request of `dashboard > profile settings > experience and education`.
    PUT/PATCH requests will be handled by another serializer below.
    """

    class Meta(DoctorExpericenceSerializer.Meta):
        fields = fields = [
            "id",
            "doctor_info",
            "establishment_name",
            "job_title",
            "start_date",
            "end_date",
            "job_description",
        ]


class DoctorExpericenceUpdateSerializerWithID(ModelSerializer):
    """
    Serializer for DoctorExpericence model which includes `id` and `operation` fields in addition.
    This serializer will only be used for PUT/PATCH request of
    `dashboard > profile settings > experience and education`.
    """

    operation = CharField(required=True, allow_null=False, write_only=True)

    def create(self, validated_data):
        validated_data.pop("operation")
        return super().create(validated_data)

    class Meta:
        model = DoctorExperience
        fields = fields = [
            "id",
            "doctor_info",
            "establishment_name",
            "job_title",
            "start_date",
            "end_date",
            "job_description",
            "operation",
        ]
        extra_kwargs = {
            "id": {"read_only": False, "required": False},
            "doctor_info": {"required": False},
            "establishment_name": {"required": False},
            "job_title": {"required": False},
            "start_date": {"required": False},
        }


class DoctorExperienceEducationSerializer(ModelSerializer):
    """
    Main serializer for `dashboard > profile settings > experience and education` page.
    Experience and education can be added updated and deleted from the single endpoint.
    This serializer will only be used for GET requests.
    """

    experience = DoctorExpericenceSerializerWithID(
        source="doctorexperience_set",
        many=True,
        required=False,
        allow_null=True,
    )
    education = DoctorEducationSerializerWithID(
        source="doctoreducation_set",
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = DoctorInfo
        fields = ("experience", "education")


class DoctorExperienceEducationUpdateSerializer(
    CustomCreateUpdateDeleteObjectOperationSerializer
):
    """
    Main serializer for `dashboard > profile settings > experience and education` page.
    Experience and education can be added updated and deleted from the single endpoint.
    This serializer will only be used for PUT/PATCH requests.
    """

    experience = DoctorExpericenceUpdateSerializerWithID(
        source="doctorexperience_set",
        many=True,
        required=False,
        allow_null=True,
    )
    education = DoctorEducationUpdateSerializerWithID(
        source="doctoreducation_set",
        many=True,
        required=False,
        allow_null=True,
    )

    def update(self, doctor_info: DoctorInfo, validated_data: dict) -> DoctorInfo:
        if "doctoreducation_set" in validated_data:
            educations = validated_data.pop("doctoreducation_set")
            self.perform_crud_operations(
                educations,
                DoctorEducationUpdateSerializerWithID,
                DoctorEducation,
                add_kwagrs={"doctor_info": doctor_info.id},
                update_kwargs={"doctor_info": doctor_info},
                delete_kwargs={"doctor_info": doctor_info},
            )

        if "doctorexperience_set" in validated_data:
            experience = validated_data.pop("doctorexperience_set")
            self.perform_crud_operations(
                experience,
                DoctorExpericenceUpdateSerializerWithID,
                DoctorExperience,
                add_kwagrs={"doctor_info": doctor_info.id},
                update_kwargs={"doctor_info": doctor_info},
                delete_kwargs={"doctor_info": doctor_info},
            )

        return doctor_info

    class Meta:
        model = DoctorInfo
        fields = ("experience", "education")


class DoctorAvailableHoursSerializerWithID(DoctorAvailableHoursSerializer):
    class Meta(DoctorAvailableHoursSerializer.Meta):
        fields = [
            "id",
            "doctor_info",
            "day_of_week",
            "start_time",
            "end_time",
        ]


class DoctorAvailableHoursUpdateSerializerWithID(ModelSerializer):
    operation = CharField(required=True, allow_null=False, write_only=True)

    def update(self, instance: DoctorAvailableHours, validated_data):
        operation = validated_data.pop("operation", None)
        if operation == "add":
            instance = DoctorAvailableHours.objects.create(**validated_data)
        elif operation == "update":
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
        elif operation == "delete":
            if instance:
                instance.delete()
        return instance

    class Meta:
        model = DoctorAvailableHours
        fields = [
            "id",
            "doctor_info",
            "day_of_week",
            "start_time",
            "end_time",
            "operation",
        ]
        extra_kwargs = {
            "id": {"read_only": False, "required": False},
            "doctor_info": {"required": False},
            "day_of_week": {"required": False},
            "start_time": {"required": False},
            "end_time": {"required": False},
        }


class DoctorSpecialtySettingsSerializer(ModelSerializer):
    """
    Serializer for `dashboard > specialties and services` page.
    """

    specialty = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_specialty(self, doctor_info: DoctorInfo) -> list:
        return list(
            doctor_info.doctorspecialty_set.all().values_list("specialty", flat=True)
        )

    def update(self, doctor_info: DoctorInfo, validated_data: dict) -> DoctorInfo:
        if "specialty" in validated_data:
            specialty = validated_data.pop("specialty")
            new_specialty = set(specialty)
            old_specialty = set(
                doctor_info.doctorspecialty_set.all().values_list(
                    "specialty", flat=True
                )
            )
            added_specialty = new_specialty - old_specialty
            removed_specialty = old_specialty - new_specialty
            DoctorSpecialty.objects.filter(
                doctor_info=doctor_info, specialty__in=removed_specialty
            ).delete()
            DoctorSpecialty.objects.bulk_create(
                [
                    DoctorSpecialty(doctor_info=doctor_info, specialty=spec)
                    for spec in added_specialty
                ]
            )
        return doctor_info

    class Meta:
        model = DoctorInfo
        fields = ["id", "specialty"]


class DoctorProfileSerializer(ModelSerializer):
    """
    Serializer for `dashboard > see my profile` page
    """

    ## TODO: implement using DoctorInfo Model
    full_name = CharField(source="user.full_name", allow_null=True)
    email = EmailField(source="user.email", allow_null=True)
    is_verified = BooleanField(
        source="user.is_verified", required=False, allow_null=True
    )
    street = CharField(source="user.street", required=False, allow_null=True)
    state = CharField(source="user.state", required=False, allow_null=True)
    city = CharField(source="user.city", required=False, allow_null=True)
    zip_code = CharField(source="user.zip_code", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = CharField(
        source="user.profile_photo", required=False, allow_null=True
    )
    avg_rating = SerializerMethodField(required=False, allow_null=True)
    qualification_suffix = SerializerMethodField(required=False, allow_null=True)
    education = DoctorEducationSerializerWithID(
        many=True,
        required=False,
        allow_null=True,
        source="doctoreducation_set",
    )
    experience = DoctorExpericenceSerializerWithID(
        many=True,
        required=False,
        allow_null=True,
        source="doctorexperience_set",
    )
    specialty = SerializerMethodField(required=False, allow_null=True)
    available_hours = DoctorAvailableHoursSerializerWithID(
        many=True,
        required=False,
        allow_null=True,
        source="doctoravailablehours_set",
    )
    review = DoctorReviewSerializer(
        many=True,
        required=False,
        allow_null=True,
        source="doctorreview_set",
    )

    def get_avg_rating(self, doctor_info: DoctorInfo) -> str:
        reviews = doctor_info.doctorreview_set.all()
        total_star = reviews.aggregate(Sum("star_count"))["star_count__sum"]
        num_reviews = reviews.count()
        return round(total_star / num_reviews, 4) if num_reviews > 0 else None

    def get_qualification_suffix(self, doctor_info: DoctorInfo) -> str:
        courses = doctor_info.doctoreducation_set.all().values_list("course", flat=True)
        return ", ".join(courses)

    def get_specialty(self, doctor_info: DoctorInfo) -> list:
        return doctor_info.doctorspecialty_set.all().values_list("specialty", flat=True)

    class Meta:
        model = DoctorInfo
        fields = [
            "id",
            "avg_rating",
            "qualification_suffix",
            "username",
            "full_name",
            "email",
            "is_verified",
            "street",
            "state",
            "city",
            "zip_code",
            "contact_no",
            "profile_photo",
            "professional_bio",
            "country",
            "gender",
            "date_of_birth",
            "identification_type",
            "identification_number",
            "identification_photo",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "awards",
            "notification_email",
            "temporary_disable",
            "accepted_insurance",
            "education",
            "experience",
            "specialty",
            "available_hours",
            "review",
        ]


class DoctorAccountSettingsSerializer(Serializer):
    old_password = CharField(required=False, allow_null=True, write_only=True)
    new_password = CharField(required=False, allow_null=True, write_only=True)
    notification_email = EmailField(required=False, allow_null=True)
    temporary_disable = BooleanField(required=False, allow_null=True)
    account_delete_password = CharField(
        required=False, allow_null=True, write_only=True
    )
    reason_to_delete = CharField(required=False, allow_null=True, write_only=True)

    def validate(self, data):
        if data.get("old_password") and not data.get("new_password"):
            raise ValidationError("you need to provide new password!")
        if data.get("new_password") and not data.get("old_password"):
            raise ValidationError("you need to provide old password!")
        if data.get("account_delete_password") and not data.get("reason_to_delete"):
            raise ValidationError("you need to provide the reason of account deletion!")
        return data
