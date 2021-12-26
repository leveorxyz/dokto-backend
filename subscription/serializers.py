from django.db.utils import NotSupportedError
from rest_framework import serializers
from stripe.api_resources import subscription
from user import models as user_models

from .mixins import SubscriptionUserTypes
from .models import SubscriptionModelMixin, SubscriptionPaymantProvider, SubscriptionType


class SubscriptionSerializer(serializers.Serializer):
    account_type = serializers.ChoiceField(SubscriptionUserTypes, write_only=True)
    account_id = serializers.UUIDField(write_only=True)
    status = serializers.BooleanField(read_only=True)

    def get_object(self) -> SubscriptionModelMixin:
        account_type = self.validated_data.get('account_type')
        account_id = self.validated_data.get('account_id')
        if account_type == SubscriptionUserTypes.CLINIC:
            return user_models.ClinicInfo.objects.get(pk=account_id)
        if account_type == SubscriptionUserTypes.DOCTOR:
            return user_models.DoctorInfo.objects.get(pk=account_id)
        if account_type == SubscriptionUserTypes.PHARMACY:
            return user_models.PharmacyInfo.objects.get(pk=account_id)
        raise NotSupportedError()

class SubscriptionChargeSerializer(SubscriptionSerializer):
    payment_method = serializers.ChoiceField(SubscriptionPaymantProvider)
    stripe_payment_method_id = serializers.CharField() # TODO: Add validations for payment gateway specific functions
    subscription_id = serializers.CharField()
    approval_url = serializers.CharField()


class ChangeMembershipSerializer(serializers.Serializer):
    change_to = serializers.ChoiceField(SubscriptionType, write_only=True)
