from rest_framework import serializers


class StripeChargeSerializer(serializers.Serializer):
    """
    Stripe Charge Serializer
    """

    order_id = serializers.IntegerField()
    token = serializers.CharField()
