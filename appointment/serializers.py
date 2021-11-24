from rest_framework.serializers import ModelSerializer, UUIDField, CharField

from .models import Appointment


class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class EncounteredListSerializer(ModelSerializer):
    account_id = UUIDField(source="patient.id")
    name = CharField(source="patient.full_name")
    address = CharField(source="patient.user.street")
    phone_number = CharField(source="patient.user.contact_no")

    class Meta:
        model = Appointment

        fields = [field.name for field in model._meta.fields] + [
            "account_id",
            "name",
            "address",
            "phone_number",
        ]
