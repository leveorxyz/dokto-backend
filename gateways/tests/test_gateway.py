from unittest.mock import patch, Mock
from django.test import TestCase

from gateways.flutterwave import FluterwaveProviver
from gateways.gateway import Gateway
from gateways.paypal import PaypalProvider
from gateways.paystack import PaystackProvider
from gateways.stripe import StripeProvider
from subscription.mixins import UserType
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider, SubscriptionPlanTypes
from user.models import User


TEST_PAYMENT_REF = 'pay_ref'
TEST_PAYMENT_GATEWAY = SubscriptionPaymantProvider.FLUTTERWAVE


def create_test_user(user_type=UserType.DOCTOR):
    return User.objects.create(email="test@gmail.com", full_name='adewale bolu', user_type=user_type)


class TestGateway(TestCase):
    def test_get_payment_gateway(self):
        provider = Gateway.get_payment_gateway(SubscriptionPaymantProvider.FLUTTERWAVE)
        self.assertEqual(type(provider), FluterwaveProviver)

        provider = Gateway.get_payment_gateway(SubscriptionPaymantProvider.PAYPAL)
        self.assertEqual(type(provider), PaypalProvider)

        provider = Gateway.get_payment_gateway(SubscriptionPaymantProvider.PAYSTACK)
        self.assertEqual(type(provider), PaystackProvider)

        provider = Gateway.get_payment_gateway(SubscriptionPaymantProvider.STRIPE)
        self.assertEqual(type(provider), StripeProvider)

    @patch('gateways.gateway.Gateway.get_provider_type', return_value=TEST_PAYMENT_GATEWAY)
    @patch('gateways.gateway.Gateway._subscribe', return_value=(TEST_PAYMENT_REF, 'http://approve'))
    def test_subscribe(self, _mock_subscribe, _mock_gateway_type):
        user = create_test_user()
        amount = 1000
        Gateway().subscribe(user, amount, SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE, 1)
        subscriptions = SubscriptionHistory.objects.filter(payment_ref=TEST_PAYMENT_REF)
        self.assertEqual(subscriptions.count(), 1)
        subscription = subscriptions.first()
        self.assertEqual(subscription.payment_method, TEST_PAYMENT_GATEWAY)
        self.assertEqual(subscription.user, user)
        self.assertEqual(subscription.amount, amount)
        self.assertEqual(subscription.active, False)
