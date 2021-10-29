from django.db import models
from django.db.models import Sum
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ListField,
)

from core.serializers import ReadWriteSerializerMethodField
from user.models import (
    DoctorAvailableHours,
    DoctorReview,
    User,
    DoctorInfo,
    DoctorSpecialty,
)
from user.serializers import (
    DoctorInfoSerializer,
    DoctorEducationSerializer,
    DoctorExpericenceSerializer,
    DoctorAvailableHoursSerializer,
    DoctorReviewSerializer,
    DoctorSpecialtySerializer,
)
from user.utils import generate_image_file_and_name


class DoctorProfileSerializer(ModelSerializer):
    avg_rating = SerializerMethodField(required=False, allow_null=True)
    qualification_suffix = SerializerMethodField(required=False, allow_null=True)
    date_of_birth = SerializerMethodField(required=False, allow_null=True)
    country = SerializerMethodField(required=False, allow_null=True)
    gender = SerializerMethodField(required=False, allow_null=True)
    professional_bio = SerializerMethodField(required=False, allow_null=True)
    education = SerializerMethodField(required=False, allow_null=True)
    experience = SerializerMethodField(required=False, allow_null=True)
    specialty = SerializerMethodField(required=False, allow_null=True)
    available_hours = SerializerMethodField(required=False, allow_null=True)
    review = SerializerMethodField(required=False, allow_null=True)

    def get_avg_rating(self, doctor: User) -> str:
        doctor_info = doctor.doctorinfo_set.first()
        reviews = doctor_info.doctorreview_set.all()
        total_star = reviews.aggregate(Sum("star_count"))["star_count__sum"]
        num_reviews = reviews.count()
        return round(total_star / num_reviews, 4) if num_reviews > 0 else None

    def get_qualification_suffix(self, doctor: User) -> str:
        doctor_info = doctor.doctorinfo_set.first()
        courses = doctor_info.doctoreducation_set.all().values_list("course", flat=True)
        return ", ".join(courses)

    def get_date_of_birth(self, doctor: User) -> str:
        return doctor.doctorinfo_set.first().date_of_birth.__str__()

    def get_country(self, doctor: User) -> str:
        return doctor.doctorinfo_set.first().country

    def get_gender(self, doctor: User) -> str:
        return doctor.doctorinfo_set.first().gender

    def get_professional_bio(self, doctor: User) -> str:
        return doctor.doctorinfo_set.first().professional_bio

    def get_education(self, doctor: User) -> list:
        doctor_info = doctor.doctorinfo_set.first()
        return DoctorEducationSerializer(
            instance=doctor_info.doctoreducation_set.all(), many=True
        ).data

    def get_experience(self, doctor: User) -> list:
        doctor_info = doctor.doctorinfo_set.first()
        return DoctorExpericenceSerializer(
            instance=doctor_info.doctorexperience_set.all(), many=True
        ).data

    def get_specialty(self, doctor: User) -> list:
        doctor_info = doctor.doctorinfo_set.first()
        return doctor_info.doctorspecialty_set.all().values_list("specialty", flat=True)

    def get_available_hours(self, doctor: User) -> list:
        doctor_info = doctor.doctorinfo_set.first()
        return DoctorAvailableHoursSerializer(
            instance=doctor_info.doctoravailablehours_set.all(), many=True
        ).data

    def get_review(self, doctor: User) -> list:
        doctor_info = doctor.doctorinfo_set.first()
        return DoctorReviewSerializer(
            instance=doctor_info.doctorreview_set.all(), many=True
        ).data

    class Meta:
        model = User
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
            "education",
            "experience",
            "specialty",
            "available_hours",
            "review",
        ]


class DoctorProfileDetailsSerializer(ModelSerializer):
    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_profile_photo(self, doctor_info: DoctorInfo) -> str:
        return doctor_info.user.profile_photo.url

    def update(self, instance, validated_data):
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


class DoctorSpecialtySettingsSerializer(ModelSerializer):
    specialty = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_specialty(self, doctor_info: DoctorInfo):
        return list(
            doctor_info.doctorspecialty_set.all().values_list("specialty", flat=True)
        )

    def update(self, doctor_info: DoctorInfo, validated_data: dict):
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
