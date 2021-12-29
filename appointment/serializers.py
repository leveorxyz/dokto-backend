import random

from rest_framework.serializers import (
    ModelSerializer,
    UUIDField,
    CharField,
    IntegerField,
)

from .models import Appointment


class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class EncounteredListSerializer(ModelSerializer):
    account_id = UUIDField(source="patient.id")
    name = CharField(source="patient.user.full_name")
    address = CharField(source="patient.user.street")
    phone_number = CharField(source="patient.user.contact_no")
    display_id = IntegerField(source="patient.display_id")

    class Meta:
        model = Appointment

        fields = [field.name for field in model._meta.fields] + [
            "account_id",
            "name",
            "address",
            "phone_number",
            "display_id",
        ]
