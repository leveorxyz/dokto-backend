from django.db.models import fields
from rest_framework.serializers import ModelSerializer, Serializer, CharField

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserLoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True)
