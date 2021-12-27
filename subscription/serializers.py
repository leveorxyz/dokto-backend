from django.db.utils import NotSupportedError
from rest_framework import serializers
from stripe.api_resources import subscription
from user import models as user_models

from .mixins import SubscriptionUserTypes
from .models import SubscriptionModelMixin, SubscriptionPaymantProvider, SubscriptionType


class SubscriptionSerializer(serializers.Serializer):
    status = serializers.BooleanField(read_only=True)

class SubscriptionChargeSerializer(SubscriptionSerializer):
    payment_method = serializers.ChoiceField(SubscriptionPaymantProvider)
    stripe_payment_method_id = serializers.CharField() # TODO: Add validations for payment gateway specific functions
    subscription_id = serializers.CharField()
    approval_url = serializers.CharField()


class ChangeMembershipSerializer(serializers.Serializer):
    change_to = serializers.ChoiceField(SubscriptionType, write_only=True)
