from typing import OrderedDict
from django.db.models import fields
from rest_framework import serializers

from .models import Wallet, WalletIncomingPayment, WalletPayout


class TransactionHistorySerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    transaction_type = serializers.CharField()
    date = serializers.DateTimeField()

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        ret['amount'] = instance[0]
        ret['transaction_type'] = instance[1]
        ret['date'] = instance[2]
        return ret


class PayoutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WalletPayout
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WalletIncomingPayment
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = '__all__'
