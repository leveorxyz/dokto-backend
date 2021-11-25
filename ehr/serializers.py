from rest_framework import serializers
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
from user.models import (
    User,
    PatientInfo,
)
from .models import AssessmentDiagnosis, MedicalNotes, PatientEncounters
from user.utils import create_user


class PatientSerializer(ModelSerializer):
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

    """
    def create(self, validated_data):
        user: User = create_user(validated_data, User.UserType.PATIENT)

        # Extract patient info
        try:
            PatientInfo.objects.create(user=user, **validated_data)
        except Exception as e:
            user.delete()
            raise e

        return user
    """

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


#
#
#
class PatientEncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientEncounters
        fields = "__all__"


class AssessmentDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentDiagnosis
        fields = "__all__"


class MedicalNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalNotes
        fields = "__all__"


# class PatientEncounterOSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     patient_id = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     provider_id = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     visit_date = serializers.DateField(required=True, blank=True, null=True)
#     location = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     #serializers.CharField(style={'base_template': 'textarea.html'})
#     signed = serializers.BooleanField(required=False, blank=True, null=True)
#     #language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     #style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#         Create and return a new `PatientEncounters` instance, given the validated data.
#         """
#         return PatientEncounters.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `PatientEncounters` instance, given the validated data.
#         """
#         instance.patient_id = validated_data.get('patient_id', instance.patient_id)
#         instance.provider_id = validated_data.get('provider_id', instance.provider_id)
#         instance.visit_date = validated_data.get('visit_date', instance.visit_date)
#         instance.location = validated_data.get('location', instance.location)
#         instance.signed = validated_data.get('signed', instance.signed)
#         instance.save()
#         return instance