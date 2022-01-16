import json
import logging
from typing import Tuple

from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from gateways.flutterwave import FluterwaveProviver
from gateways.gateway import Gateway
from gateways.paypal import PaypalProvider
from gateways.paystack import PaystackProvider
from gateways.stripe import StripeProvider
from subscription.utils import get_subscription_user
from user.models import User
from .models import SubscriptionHistoryPayment, SubscriptionModelMixin, SubscriptionPlanTypes, SubscriptionType

from .serializers import ChangeMembershipSerializer, SubscriptionChargeSerializer, SubscriptionSerializer


# Create your views here.
class SubscriptionBaseView(GenericViewSet):
    serializer_class = SubscriptionSerializer

    def __init__(self, *args, **kwargs):
        super(SubscriptionBaseView, self).__init__(*args, **kwargs)
        self.object = None

    def validate(self) -> Tuple[bool, str]:
        # raise exception if not possible
        return True, ""

    def handle(self, serializer: SubscriptionSerializer):
        raise NotImplemented()

    def get_object(self) -> SubscriptionModelMixin:
        if not self.object:
            user: User = self.request.user
            self.object = get_subscription_user(user)
        return self.object

    def create(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        is_valid, reason = self.validate()
        if not is_valid:
            raise ValidationError([reason])
        res = self.handle(self.serializer)
        return Response(res, status=status.HTTP_200_OK)


class SubscriptionView(SubscriptionBaseView):
    serializer_class = SubscriptionChargeSerializer

    def validate(self):
        return self.get_object().can_subscribe()

    def handle(self, serializer):
        obj = self.get_object()
        payment_method = self.serializer.validated_data.get('payment_method')
        amount_to_pay, plan_type, quantity = obj.get_subscription_info()
        sub_id, approval_url = Gateway.get_payment_gateway(payment_method).subscribe(self.request.user, amount_to_pay, plan_type, quantity)
        # self.serializer = SubscriptionChargeSerializer(data={'subscription_id': sub_id, 'approval_url': approval_url})
        return {'approval_url': approval_url, 'payment_method': payment_method, 'status': True}


class UnsubscribeView(SubscriptionBaseView):

    def validate(self):
        return self.get_object().can_unsubscribe()

    def handle(self, _serializer):
        obj = self.get_object()
        payment_method = obj.current_subscription.payment_method
        Gateway.get_payment_gateway(payment_method).cancel_subscription(obj)
        return {'status': True}


class ChangeSubscriptionView(SubscriptionBaseView):
    serializer_class = ChangeMembershipSerializer

    def validate(self):
        if self.get_object().subscription_type == SubscriptionType.MEMBERSHIP:
            return self.get_object().can_use_pay_as_you_go(self.serializer.change_to)
        else:
            return self.get_object().can_use_membership(self.serializer.change_to)

    def handle(self, serializer: ChangeMembershipSerializer):
        self.get_object().change_membership_type(serializer.change_to)


class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]
    provider: Gateway = None

    def post(self, *args, **kwargs):
        try:
            # TODO: Remove try block and replace with celery task
            self.provider.handle_webhook(self.request)
        except Exception:
            pass
        logging.info("Webhook request :" + json.dumps(self.request.data))
        return Response({})


class FlutterwaveWebhook(PaymentWebhookView):
    provider = FluterwaveProviver()


class PaystackWebhook(PaymentWebhookView):
    provider = PaystackProvider()


class StripeWebhook(PaymentWebhookView):
    provider = StripeProvider()


class PaypalWebhook(PaymentWebhookView):
    provider = PaypalProvider()


class SubscriptionPaymentsView(GenericViewSet, ListModelMixin):
    serializer_class = SubscriptionHistoryPayment

    def get_queryset(self):
        return SubscriptionHistoryPayment.objects.filter(subscription__user=self.request.user)
