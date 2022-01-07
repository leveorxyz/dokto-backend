import logging
from typing import Tuple

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
    paused = models.BooleanField(default=False)
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

    def set_paused(self):
        self.paused = True
        subscription_object = SubscriptionModelMixin.get_subscription_user(self.user)
        subscription_object.confirm_subscription_cancelled(self)
        self.save()

class SubscriptionModelMixin(models.Model):
    subscription_type = models.CharField(
        max_length=1, choices=SubscriptionType.choices, default=SubscriptionType.PAY_AS_YOU_GO
    )
    is_active = models.BooleanField(default=False)
    current_subscription = models.ForeignKey(SubscriptionHistory, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract=True

    @property
    def is_subscription_active(self):
        return self.is_active # TODO: Is it possible to use a new field name?

    def can_subscribe(self) -> Tuple[bool, str]:
        if not self.current_subscription and  self.subscription_type == SubscriptionType.MEMBERSHIP:
            return True, ""
        return False, "Doctor not on membership plan or is currently subscribed"

    def can_unsubscribe(self) -> Tuple[bool, str]:
        if self.current_subscription:
            return True, ""
        return False, "Doctor is current not in any active subscription"

    def can_use_membership(self, membership_type) -> Tuple[bool, str]:
        return True, ""

    def can_use_pay_as_you_go(self):
        return True, ""

    def confirm_subscription_extended(self, subscription):
        if self.current_subscription and self.current_subscription != subscription:
            logging.error(f"Another subscription is currently active for user {self.user.id}")
            return
        self.is_subscription_active = True
        self.current_subscription = subscription
        self.save()


    def confirm_subscription_cancelled(self, subscription):
        if subscription != self.current_subscription:
            logging.error(f"Another subscription is currently active for user {self.user.id}")
            return
        self.is_subscription_active = False
        self.current_subscription = None
        self.save()

    def change_membership_type(self):
        pass

    def get_subscription_info(self) -> Tuple[int, str, int]:
        return 0, SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE, 1


class SubscriptionHistoryPayment(CoreModel):
    subscription = models.ForeignKey(SubscriptionHistory, on_delete=models.CASCADE)
    payment_ref = models.CharField(max_length=30)
    start = models.DateField()
    end = models.DateField()