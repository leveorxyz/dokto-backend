from django.db import models
from django.db.models import Sum
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from core.serializers import ReadWriteSerializerMethodField
from user.models import (
    DoctorAvailableHours,
    DoctorReview,
    User,
    DoctorInfo,
)
from user.serializers import (
    DoctorInfoSerializer,
    DoctorEducationSerializer,
    DoctorExpericenceSerializer,
    DoctorAvailableHoursSerializer,
    DoctorReviewSerializer,
)


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
