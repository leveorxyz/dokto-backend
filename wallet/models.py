from django.db import models
from django.db.models.enums import TextChoices
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel
from ehr.models import PatientEncounters
from user.models import User

# Create your models here.

class PaymentGateway(TextChoices):
    PAYPAL = 'P', _('paypal')
    STRIPE = 'S', _('stripe')
    FLUTTERWAVE = 'F', _('flutterwave')
    PAYSTACK = 'Y', _('paystack')


class PaymentStatus(TextChoices):
    PENDING = 'P', _('pending')
    SUCCESS = 'S', _('success')
    FAILED = 'F', _('failed')


class Wallet(CoreModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def disburse_to_wallet(self, amount, ehr):
        # TODO: Consider using subscription to determine amount to add to wallet
        # TODO: Considering moving it to utils
        WalletIncomingPayment.objects.create(wallet=self, ehr=ehr, amount_charged=amount, amount=amount, status=PaymentStatus.SUCCESS)
        self.amount += amount
        self.save()
        # TODO: Add unit tests


class WalletPayout(CoreModel):
    wallet = ForeignKey(Wallet, on_delete=models.Case)
    amount = models.IntegerField()
    gateway = models.CharField(choices=PaymentGateway.choices, max_length=3)
    gateway_ref = models.CharField(max_length=30, null=True)
    status = models.CharField(choices=PaymentStatus.choices, max_length=2, default=PaymentStatus.PENDING)

class WalletIncomingPayment(CoreModel):
    wallet = ForeignKey(Wallet, on_delete=models.Case)
    ehr = models.ForeignKey(PatientEncounters, on_delete=models.CASCADE, null=True, blank=True)
    amount_charged = models.IntegerField()
    amount = models.IntegerField()  #Check: Q: Do we use subscription type as at the time of creating the ehr or subscription type as at the time of adding payment
    status = models.CharField(choices=PaymentStatus.choices, max_length=2, default=PaymentStatus.PENDING)
