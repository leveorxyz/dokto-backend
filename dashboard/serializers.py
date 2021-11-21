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

from core.serializers import ReadWriteSerializerMethodField
from user.models import (
    DoctorAvailableHours,
    User,
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
from user.utils import generate_image_file_and_name


class DoctorProfileDetailsSerializer(ModelSerializer):
    """
    Serializes the `Dashboard > Profile Settings > Profile Details` page
    """

    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_profile_photo(self, doctor_info: DoctorInfo) -> str:
        return doctor_info.user.profile_photo.url

    def update(self, instance: DoctorInfo, validated_data: dict) -> DoctorInfo:
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user = instance.user
            full_name = user_data.get("full_name", user.full_name)
            contact_no = user_data.get("contact_no", user.contact_no)
            user.full_name = full_name
            user.contact_no = contact_no
            user.save()
        if "profile_photo" in validated_data:
            profile_photo_data = validated_data.pop("profile_photo")
            user = instance.user
            file_name, file = generate_image_file_and_name(profile_photo_data, user.id)
            user.profile_photo.delete(save=True)
            user.profile_photo.save(file_name, file, save=True)
            user.save()
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

    certificate = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_certificate(self, doctor_education: DoctorEducation):
        return doctor_education.certificate.url

    class Meta(DoctorEducationSerializer.Meta):
        fields = [
            "id",
            "doctor_info",
            "course",
            "year",
            "college",
            "certificate",
        ]


class DoctorEducationUpdateSerializerWithID(ModelSerializer):
    """
    Serializer for DoctorEducation model which includes `id` and `operation` fields in addition.
    This serializer will only be used for PUT/PATCH request of
    `dashboard > profile settings > experience and education`.
    """

    operation = CharField(required=True, allow_null=False, write_only=True)
    certificate = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_certificate(self, doctor_education: DoctorEducation):
        return doctor_education.certificate.url

    class Meta:
        model = DoctorEducation
        fields = [
            "id",
            "doctor_info",
            "course",
            "year",
            "college",
            "certificate",
            "operation",
        ]
        extra_kwargs = {
            "id": {"read_only": False, "required": False},
            "doctor_info": {"required": False},
            "course": {"required": False},
            "year": {"required": False},
            "college": {"required": False},
            "certificate": {"required": False},
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


class DoctorExperienceEducationUpdateSerializer(ModelSerializer):
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
            added = [
                {k: v for k, v in education.items() if k != "operation"}
                for education in educations
                if education.get("operation") == "add"
            ]
            updated = [
                {k: v for k, v in education.items() if k != "operation"}
                for education in educations
                if education.get("operation") == "update"
            ]
            deleted = [
                education.get("id")
                for education in educations
                if education.get("operation") == "delete" and education.get("id")
            ]
            delete_queryset = DoctorEducation.objects.filter(
                doctor_info=doctor_info, id__in=deleted
            )
            for instance in delete_queryset:
                instance.delete()
            for education_data in added:
                doctor_education_serializer = DoctorEducationSerializer(
                    data={"doctor_info": doctor_info.id, **education_data}
                )
                doctor_education_serializer.is_valid(raise_exception=True)
                doctor_education_serializer.save()
            for education_data in updated:
                if "id" in education_data:
                    education_instance = get_object_or_404(
                        DoctorEducation, id=education_data.pop("id")
                    )
                    for key, value in education_data.items():
                        if key == "certificate":
                            certificate_data = education_data.get("certificate")
                            file_name, file = generate_image_file_and_name(
                                certificate_data, doctor_info.id
                            )
                            education_instance.certificate.delete(save=True)
                            education_instance.certificate.save(
                                file_name, file, save=True
                            )
                            education_instance.save()
                        elif hasattr(education_instance, key):
                            setattr(education_instance, key, value)
                    education_instance.save()

        if "doctorexperience_set" in validated_data:
            experiences = validated_data.pop("doctorexperience_set")
            added = [
                {k: v for k, v in experience.items() if k != "operation"}
                for experience in experiences
                if experience.get("operation") == "add"
            ]
            updated = [
                {k: v for k, v in experience.items() if k != "operation"}
                for experience in experiences
                if experience.get("operation") == "update"
            ]
            deleted = [
                experience.get("id")
                for experience in experiences
                if experience.get("operation") == "delete" and experience.get("id")
            ]
            DoctorExperience.objects.filter(
                doctor_info=doctor_info, id__in=deleted
            ).delete()
            for experience_data in added:
                doctor_experience_serializer = DoctorExpericenceSerializer(
                    data={"doctor_info": doctor_info.id, **experience_data}
                )
                doctor_experience_serializer.is_valid(raise_exception=True)
                doctor_experience_serializer.save()

            for experience_data in updated:
                if "id" in experience_data:
                    experience_instance = get_object_or_404(
                        DoctorExperience, id=experience_data.pop("id")
                    )
                    for key, value in experience_data.items():
                        if hasattr(experience_instance, key):
                            setattr(experience_instance, key, value)
                    experience_instance.save()
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
    profile_photo = SerializerMethodField(required=False, allow_null=True)
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

    def get_profile_photo(self, doctor_info: DoctorInfo) -> str:
        return settings.BACKEND_URL + doctor_info.user.profile_photo.url

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
