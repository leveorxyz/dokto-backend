
from rest_framework import serializers


class StripeChargeSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    token = serializers.CharField()
