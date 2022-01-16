from rest_framework import serializers

from .mixins import SubscriptionUserTypes
from .models import SubscriptionModelMixin, SubscriptionHistoryPayment, SubscriptionPaymantProvider, SubscriptionType


class SubscriptionSerializer(serializers.Serializer):
    status = serializers.BooleanField(read_only=True)

class SubscriptionChargeSerializer(SubscriptionSerializer):
    payment_method = serializers.ChoiceField(SubscriptionPaymantProvider)
    approval_url = serializers.CharField(read_only=True)


class ChangeMembershipSerializer(serializers.Serializer):
    change_to = serializers.ChoiceField(SubscriptionType, write_only=True)

class SubscriptionHistoryPayment(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionHistoryPayment
        fields = '__all__'
