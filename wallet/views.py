from django.db.models.expressions import Value
from django.db.models.fields import CharField
from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from wallet.models import PaymentStatus, Wallet, WalletIncomingPayment, WalletPayout
from wallet.serializers import PaymentSerializer, PayoutSerializer, TransactionHistorySerializer, WalletSerializer

# Create your views here.
class TransactionHistoryView(GenericViewSet, ListModelMixin):
    serializer_class = TransactionHistorySerializer

    def get_queryset(self):
        wallet = Wallet.objects.get(user=self.request.user)
        payouts = WalletPayout.objects.annotate(transaction_type=Value('debit', output_field=CharField())).filter(wallet=wallet).filter(status=PaymentStatus.SUCCESS).values_list('amount', 'transaction_type', 'created_at')
        payments = WalletIncomingPayment.objects.annotate(transaction_type=Value('credit', output_field=CharField())).filter(wallet=wallet).filter(status=PaymentStatus.SUCCESS).values_list('amount', 'transaction_type', 'created_at')
        query = payouts.union(payments).order_by('-created_at')
        return query

class PayoutHistoryView(GenericViewSet, ListModelMixin):
    serializer_class = PayoutSerializer

    def get_queryset(self):
        wallet = Wallet.objects.get(user=self.request.user)
        return WalletPayout.objects.filter(wallet=wallet).order_by('-created_at')


class PaymentHistoryView(GenericViewSet, ListModelMixin):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        wallet = Wallet.objects.get(user=self.request.user)
        return WalletIncomingPayment.objects.filter(wallet=wallet).order_by('-created_at')

class WalletDetailView(GenericViewSet, RetrieveModelMixin):
    serializer_class = WalletSerializer

    def get_object(self, *args, **kwargs):
        return Wallet.objects.get(user=self.request.user)
