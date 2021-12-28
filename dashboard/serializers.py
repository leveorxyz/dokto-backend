from django.db.models import Sum
from rest_framework.fields import DateField, ListField, URLField
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    SerializerMethodField,
    CharField,
    EmailField,
    BooleanField,
    ChoiceField,
)
from rest_framework.exceptions import ValidationError

from core.serializers import (
    AbstractAccountSettingsSerializer,
    ReadWriteSerializerMethodField,
    CustomCreateUpdateDeleteObjectOperationSerializer,
    FieldListUpdateSerializer,
)
from user.models import (
    ClinicInfo,
    DoctorAcceptedInsurance,
    DoctorAvailableHours,
    DoctorInfo,
    DoctorLanguage,
    DoctorSpecialty,
    DoctorEducation,
    DoctorExperience,
    PatientInfo,
    PharmacyInfo,
)
from user.serializers import (
    DoctorReviewSerializer,
)


class DoctorProfileDetailsSerializer(ModelSerializer):
    """
    Serializes the `Dashboard > Profile Settings > Profile Details` page
    """

    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = CharField(
        source="user.profile_photo", required=False, allow_null=True
    )
    date_of_birth = DateField(required=False, allow_null=True)
    gender = ChoiceField(
        source="user.gender", choices=DoctorInfo.Gender.choices, required=False
    )
    email = EmailField(source="user.email", read_only=True)
    street = CharField(source="user.street", required=False)
    city = CharField(source="user.city", required=False)
    state = CharField(source="user.state", required=False)
    country = CharField(required=False)
    zip_code = CharField(source="user.zip_code", required=False)

    def update(self, instance: DoctorInfo, validated_data: dict) -> DoctorInfo:
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            instance.user.update_from_validated_data(user_data)
            if "profile_photo" in user_data:
                profile_photo_data = user_data.pop("profile_photo")
                instance.user.profile_photo = profile_photo_data

        instance.update_from_validated_data(validated_data)
        return instance

    class Meta:
        model = DoctorInfo
        fields = [
            "full_name",
            "gender",
            "contact_no",
            "profile_photo",
            "professional_bio",
            "email",
            "street",
            "city",
            "country",
            "zip_code",
            "date_of_birth",
            "state",
        ]


class DoctorEducationSerializerWithID(ModelSerializer):

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
            "doctor_info": {"required": False, "write_only": True},
            "course": {"required": False},
            "year": {"required": False},
            "college": {"required": False},
        }


class DoctorExpericenceSerializerWithID(ModelSerializer):
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
            "doctor_info": {"required": False, "write_only": True},
            "establishment_name": {"required": False},
            "job_title": {"required": False},
            "start_date": {"required": False},
        }


class DoctorExperienceEducationSerializer(
    CustomCreateUpdateDeleteObjectOperationSerializer
):
    """
    Main serializer for `dashboard > profile settings > experience and education` page.
    Experience and education can be added updated and deleted from the single endpoint.
    This serializer will only be used for PUT/PATCH requests.
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

    def update(self, doctor_info: DoctorInfo, validated_data: dict) -> DoctorInfo:
        if "doctoreducation_set" in validated_data:
            educations = validated_data.pop("doctoreducation_set")
            self.perform_crud_operations(
                educations,
                DoctorEducationSerializerWithID,
                DoctorEducation,
                add_kwagrs={"doctor_info": doctor_info.id},
                update_kwargs={"doctor_info": doctor_info},
                delete_kwargs={"doctor_info": doctor_info},
            )

        if "doctorexperience_set" in validated_data:
            experience = validated_data.pop("doctorexperience_set")
            self.perform_crud_operations(
                experience,
                DoctorExpericenceSerializerWithID,
                DoctorExperience,
                add_kwagrs={"doctor_info": doctor_info.id},
                update_kwargs={"doctor_info": doctor_info},
                delete_kwargs={"doctor_info": doctor_info},
            )

        return doctor_info

    class Meta:
        model = DoctorInfo
        fields = ("experience", "education")


class DoctorAvailableHoursSerializerWithID(ModelSerializer):
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
            "doctor_info": {"required": False, "write_only": True},
            "day_of_week": {"required": False},
            "start_time": {"required": False},
            "end_time": {"required": False},
        }


class DoctorSpecialtySettingsSerializer(FieldListUpdateSerializer):
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
            _ = self.perform_list_field_update(
                validated_data.pop("specialty"),
                DoctorSpecialty,
                "specialty",
                {"doctor_info": doctor_info},
            )
        return doctor_info

    class Meta:
        model = DoctorInfo
        fields = ["specialty"]


class DoctorProfileSerializer(ModelSerializer):
    """
    Serializer for `dashboard > see my profile` page
    """

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


class DoctorAccountSettingsSerializer(AbstractAccountSettingsSerializer):
    class Meta:
        model = DoctorInfo
        fields = AbstractAccountSettingsSerializer.Meta.fields


class PatientProfileDetailsSerializer(ModelSerializer):
    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = CharField(
        source="user.profile_photo", required=False, allow_null=True
    )
    date_of_birth = DateField(required=False, allow_null=True)
    gender = ChoiceField(
        source="user.gender", choices=DoctorInfo.Gender.choices, required=False
    )
    email = EmailField(source="user.email", read_only=True)
    street = CharField(source="user.street", required=False)
    city = CharField(source="user.city", required=False)
    state = CharField(source="user.state", required=False)
    zip_code = CharField(source="user.zip_code", required=False)

    def update(self, instance: PatientInfo, validated_data: dict) -> PatientInfo:
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            instance.user.update_from_validated_data(user_data)
            if "profile_photo" in user_data:
                profile_photo_data = user_data.pop("profile_photo")
                instance.user.profile_photo = profile_photo_data

        instance.update_from_validated_data(validated_data)
        return instance

    class Meta:
        model = PatientInfo
        fields = [
            "full_name",
            "gender",
            "contact_no",
            "profile_photo",
            "email",
            "street",
            "city",
            "zip_code",
            "date_of_birth",
            "state",
        ]


class PatientAccountSettingsSerializer(AbstractAccountSettingsSerializer):
    class Meta:
        model = PatientInfo
        fields = AbstractAccountSettingsSerializer.Meta.fields


class DoctorProfessionalProfileSerializer(FieldListUpdateSerializer):
    license_file = CharField(required=False, allow_null=True)
    language = ReadWriteSerializerMethodField(required=False, allow_null=True)

    def get_language(self, doctor_info: DoctorInfo) -> list:
        return doctor_info.doctorlanguage_set.all().values_list("language", flat=True)

    def update(self, instance, validated_data):
        if "license_file" in validated_data:
            instance.license_file = validated_data.pop("license_file")
        if "language" in validated_data:
            _ = self.perform_list_field_update(
                validated_data.pop("language"),
                DoctorLanguage,
                "language",
                {"doctor_info": instance},
            )

        return super().update(instance, validated_data)

    class Meta:
        model = DoctorInfo
        fields = [
            "professional_bio",
            "license_file",
            "license_expiration",
            "language",
        ]
        extra_kwargs = {field: {"required": False} for field in fields}


class DoctorAcceptedInsuranceSerializer(FieldListUpdateSerializer):
    accepted_insurance = ReadWriteSerializerMethodField(required=False, allow_null=True)
    accept_all_insurance = ListField(
        child=CharField(), required=False, allow_null=True, write_only=True
    )

    def get_accepted_insurance(self, doctor_info: DoctorInfo) -> list:
        return doctor_info.doctoracceptedinsurance_set.all().values_list(
            "insurance", flat=True
        )

    def validate(self, attrs):
        if "accepted_insurance" not in attrs and "accept_all_insurance" not in attrs:
            raise ValidationError(
                "You need to provide accepted insurance or accept all insurance"
            )
        if "accept_all_insurance" in attrs and attrs["accept_all_insurance"] != ["all"]:
            raise ValidationError("You can only accept all insurance")
        if "accept_all_insurance" in attrs:
            attrs["accepted_insurance"] = ["all"]
        return super().validate(attrs)

    def update(self, instance, validated_data):
        self.perform_list_field_update(
            validated_data.pop("accepted_insurance"),
            DoctorAcceptedInsurance,
            "insurance",
            {"doctor_info": instance},
        )
        return instance

    class Meta:
        model = DoctorInfo
        fields = ["accepted_insurance", "accept_all_insurance"]


class PharmacyAccountSettingsSerializer(AbstractAccountSettingsSerializer):
    class Meta:
        model = PharmacyInfo
        fields = AbstractAccountSettingsSerializer.Meta.fields


class ClinicAccountSettingsSerializer(AbstractAccountSettingsSerializer):
    class Meta:
        model = ClinicInfo
        fields = AbstractAccountSettingsSerializer.Meta.fields


class ClinicProfileDetailsSerializer(ModelSerializer):
    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = CharField(
        source="user.profile_photo", required=False, allow_null=True
    )
    email = EmailField(source="user.email", read_only=True)
    street = CharField(source="user.street", required=False)
    city = CharField(source="user.city", required=False)
    state = CharField(source="user.state", required=False)
    zip_code = CharField(source="user.zip_code", required=False)

    def update(self, instance: ClinicInfo, validated_data: dict) -> ClinicInfo:
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            instance.user.update_from_validated_data(user_data)
            if "profile_photo" in user_data:
                profile_photo_data = user_data.pop("profile_photo")
                instance.user.profile_photo = profile_photo_data

        instance.update_from_validated_data(validated_data)
        return instance

    class Meta:
        model = ClinicInfo
        fields = [
            "full_name",
            "contact_no",
            "profile_photo",
            "email",
            "street",
            "city",
            "zip_code",
            "state",
            "website",
        ]
        extra_kwargs = {"website": {"required": False}}


class ClinicLicenseSerializer(ModelSerializer):
    license_file = CharField(required=False, allow_null=True)

    class Meta:
        model = ClinicInfo
        fields = ["license_file", "license_expiration"]


class PharmacyProfileSettingsSerializer(ModelSerializer):
    full_name = CharField(source="user.full_name", required=False, allow_null=True)
    contact_no = CharField(source="user.contact_no", required=False, allow_null=True)
    profile_photo = CharField(
        source="user.profile_photo", required=False, allow_null=True
    )
    email = EmailField(source="user.email", read_only=True)
    street = CharField(source="user.street", required=False)
    city = CharField(source="user.city", required=False)
    state = CharField(source="user.state", required=False)
    zip_code = CharField(source="user.zip_code", required=False)

    def update(self, instance: PharmacyInfo, validated_data: dict) -> PharmacyInfo:
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            instance.user.update_from_validated_data(user_data)
            if "profile_photo" in user_data:
                profile_photo_data = user_data.pop("profile_photo")
                instance.user.profile_photo = profile_photo_data

        instance.update_from_validated_data(validated_data)
        return instance

    class Meta:
        model = PharmacyInfo
        fields = [
            "full_name",
            "contact_no",
            "profile_photo",
            "email",
            "street",
            "city",
            "zip_code",
            "state",
            "website",
            "bio",
        ]
        extra_kwargs = {"website": {"required": False}, "bio": {"required": False}}


class PharmacyLicenseSerializer(ModelSerializer):
    license_file = CharField(required=False, allow_null=True)

    class Meta:
        model = PharmacyInfo
        fields = ["license_file", "license_expiration"]


class PharmacyProfileDetailsSerializer(ModelSerializer):
    profile_photo = CharField(source="user.profile_photo")
    full_name = CharField(source="user.full_name")
    contact_no = CharField(source="user.contact_no")
    email = EmailField(source="user.email")
    address = SerializerMethodField()

    def get_address(self, obj: PharmacyInfo) -> str:
        address_fields = ["street", "city", "state", "zip_code"]
        return ",".join(
            [
                getattr(obj.user, field)
                for field in address_fields
                if getattr(obj.user, field)
            ]
        )

    class Meta:
        model = PharmacyInfo
        fields = [
            "profile_photo",
            "full_name",
            "contact_no",
            "email",
            "address",
            "bio",
            "website",
            "services",
        ]
