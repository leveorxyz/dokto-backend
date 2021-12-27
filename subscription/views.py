from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from gateways.flutterwave import FluterwaveProviver
from gateways.gateway import Gateway
from gateways.paypal import PaypalProvider
from gateways.paystack import PaystackProvider
from subscription.utils import get_subscription_user
from user.models import User
from .models import SubscriptionModelMixin

from .serializers import ChangeMembershipSerializer, SubscriptionChargeSerializer, SubscriptionSerializer


# Create your views here.
class SubscriptionBaseView(GenericViewSet):
    serializer_class = SubscriptionSerializer

    def validate(self) -> tuple[bool, str]:
        # raise exception if not possible
        return True, ""

    def handle(self, serializer: SubscriptionSerializer):
        raise NotImplemented()

    def get_object(self) -> SubscriptionModelMixin:
        if not self.object:
            user: User = self.request.user
            self.object = get_subscription_user(user)
        return self.object

    def check_permission(self, request):
        if self.get_object().user != self.user:
            raise self.permission_denied(request)

    def create(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        is_valid, reason = self.validate()
        if not is_valid:
            raise ValidationError([reason])
        self.handle(self.serializer)
        return Response(self.serializer.data, status=status.HTTP_200_OK)


class SubscriptionView(SubscriptionBaseView):
    serializer_class = SubscriptionChargeSerializer

    def validate(self):
        self.get_object().can_subscribe()

    def handle(self):
        obj = self.get_object()
        payment_method = self.serializer.validated_data.get('payment_method')
        amount_to_pay, plan_type, quantity = obj.get_subscription_info()
        sub_id, approval_url = Gateway.get_payment_gateway(payment_method).subscribe(self.request.user, amount_to_pay, plan_type, quantity)
        return Response({'subscription_id': sub_id, 'approval_url': approval_url})


class UnsubscribeView(SubscriptionBaseView):

    def validate(self):
        self.get_object().can_unsubscribe()


class ChangeSubscriptionView(SubscriptionBaseView):
    serializer_class = ChangeMembershipSerializer

    def validate(self):
        return self.get_object().can_unsubscribe(self.serializer.change_to)

    def handle(self, serializer: ChangeMembershipSerializer):
        self.get_object().change_membership_type(serializer.change_to)


class FlutterwaveWebhook(APIView):
    permission_classes = [permissions.AllowAny]
    # def check_permissions(self, request):
    #     return
    # TODO: Handle permission
    def post(self, *args, **kwargs):
        FluterwaveProviver().handle_webhook(self.request)
        return Response({})


class PaystackWebhook(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        PaystackProvider().handle_webhook(self.request)
        return Response({})


class StripeWebhook(APIView):
    def post(self):
        pass


class PaypalWebhook(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        PaypalProvider().handle_webhook(self.request)
        return Response({})
