from datetime import datetime, timedelta
from re import sub
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel

SubscriptionHistory = None

class SubscriptionPlanTypes:
    DOTOR_SUSBCRIPTION_TYPE = 'DS'
    DOCTOR_WITH_HOME_SERVICE = 'DH'
    PHARMACY_SUBSCRIPTION_PLAN = 'PS'
    CLINIC_SUBSCRIPTION_PLAN = 'CS'

SubscriptionProducts = []
class SubscriptionType(models.TextChoices):
    MEMBERSHIP = "M", _("membership")
    PAY_AS_YOU_GO = "P", _("pay as you go")

class SubscriptionPaymantProvider(models.TextChoices):
    PAYSTACK = "T", _("paystack")
    FLUTTERWAVE = "F", _("flutterwave")
    STRIPE = "S", _("stripe")
    PAYPAL = "P", _("paypal")

class SubscriptionHistory(CoreModel):
    payment_method = models.CharField(max_length=3, choices=SubscriptionPaymantProvider.choices)
    payment_ref = models.CharField(max_length=30)
    subscription_start = models.DateField(null=True)
    subscription_end = models.DateField(null=True)
    extra_gateway_values = models.CharField(max_length=100, default='')
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    active = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    amount = models.IntegerField()
    
    def add_new_payment(self, ref, start, end):
        self.paid = True
        today = datetime.today()
        if not self.subscription_end:
            self.subscription_end = end
        if self.subscription_end < end:
            self.subscription_end = end
        if self.subscription_end > today:
            self.active = True
        if not self.subscription_start:
            self.subscription_start = start
        self.save()
        SubscriptionHistoryPayment.objects.create(subscription=self, payment_ref=ref, start=start, end=end)
        subscription_object = SubscriptionModelMixin.get_subscription_user(self.user)
        subscription_object.confirm_subscription_extended()

class SubscriptionModelMixin(models.Model):
    subscription_type = models.CharField(
        max_length=1, choices=SubscriptionType.choices, default=SubscriptionType.PAY_AS_YOU_GO
    )
    is_active = models.BooleanField(default=False)
    current_subscription = models.ForeignKey(SubscriptionHistory, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract=True

    def can_subscribe(self) -> tuple[bool, str]:
        if not self.is_active and  self.subscription_type == SubscriptionType.MEMBERSHIP:
            return True, ""
        return False, "Doctor not on membership plan or is currently subscribed"

    def can_unsubscribe(self) -> tuple[bool, str]:
        if not self.active:
            return True, ""
        return False, "Doctor is current not in any active subscription"

    def can_use_membership(self, membership_type) -> tuple[bool, str]:
        return True, ""

    def can_use_pay_as_you_go(self):
        return True, ""

    def confirm_subscription_extended(self, subscription):
        self.is_active = True
        self.save()

    def confirm_subscription_cancelled(self):
        pass

    def change_membership_type(self):
        pass

    def get_subscription_info(self) -> tuple[int, str, int]:
        return 0, SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE, 1
    # from user.models import User



class SubscriptionHistoryPayment(CoreModel):
    subscription = models.ForeignKey(SubscriptionHistory, on_delete=models.CASCADE)
    payment_ref = models.CharField(max_length=30)
    start = models.DateField()
    end = models.DateField()
