from datetime import datetime, timedelta
from re import sub
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel

class SubscriptionPlanTypes:
    DOTOR_SUSBCRIPTION_TYPE = 'DS'
    DOCTOR_WITH_HOME_SERVICE = 'DH'
    PHARMACY_SUBSCRIPTION_PLAN = 'PS'
    CLINIC_SUBSCRIPTION_PLAN = 'CS'

SubscriptionProducts = []
class SubscriptionType(models.TextChoices):
    MEMBERSHIP = "M", _("membership")
    PAY_AS_YOU_GO = "P", _("pay as you go")


class SubscriptionModelMixin(models.Model):
    subscription_type = models.CharField(
        max_length=1, choices=SubscriptionType.choices, default=SubscriptionType.PAY_AS_YOU_GO
    )
    is_active = models.BooleanField(default=False)

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

    def confirm_subscription_extended(self):
        self.is_active = True
        self.save()

    def confirm_subscription_cancelled(self):
        pass

    def change_membership_type(self):
        pass

    def get_subscription_info(self) -> tuple[int, str, int]:
        return 0, SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE, 1
    # from user.models import User


class SubscriptionPaymantProvider(models.TextChoices):
    PAYSTACK = "T", _("paystack")
    FLUTTERWAVE = "F", _("flutterwave")
    STRIPE = "S", _("stripe")
    PAYPAL = "P", _("paypal")


class SubscriptionHistory(CoreModel):
    payment_method = models.CharField(max_length=3, choices=SubscriptionPaymantProvider.choices)
    payment_ref = models.CharField(max_length=30)
    subscription_start = models.DateField()
    subscription_end = models.DateField()
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    paid = models.BooleanField(default=False)
    
    def set_paid(self):
        # TODO: Unit tests around all possible issues
        subscription = self
        if self.paid:
            subscription = SubscriptionHistory()
            subscription.user = self.user
            subscription.payment_ref = self.payment_ref
            subscription.payment_method = self.payment_method
        subscription.paid = True
        today = datetime.now().date()
        last_active_subscription = SubscriptionHistory.objects.filter(user=subscription.user).filter(paid=True).order_by('-subscription_end').first()
        if not last_active_subscription or last_active_subscription.subscription_end < today:
            subscription.subscription_start = today
        else:
            subscription.subscription_start = last_active_subscription.subscription_end + timedelta(days=1)
        subscription.subscription_end = subscription.subscription_start + timedelta(days=30)
        subscription.save()
        subscription_object = SubscriptionModelMixin.get_subscription_user(subscription.user)
        subscription_object.confirm_subscription_extended()
