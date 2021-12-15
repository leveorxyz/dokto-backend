from rest_framework.serializers import Serializer, UUIDField


class OnboardSerializer(Serializer):
    doctor_id = UUIDField()
