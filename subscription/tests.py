import json
from unittest.mock import Mock, patch
from django.test import TestCase
from subscription.mixins import UserType
from subscription.models import SubscriptionType
from subscription.providers import FluterwaveProviver, Provider, StripeProvider, stripe
from subscription.serializers import SubscriptionSerializer
from subscription.utils import PayPalAPI, create_paypal_plan

from user.models import ClinicInfo, DoctorInfo, PatientInfo, PharmacyInfo, User

FLUTTERWAVE_WEBHOOK_PAYLOAD = {
            "id": 2767577,
            "txRef": "69c7a6a1-97e0-49c3-a4b7-483260d816da",
            "flwRef": "FLW-MOCK-3aa480ac93a46883f384d63eb8485796",
            "orderRef": "URF_1640341854577_3192235",
            "paymentPlan": 16614,
            "paymentPage": None,
            "createdAt": "2021-12-24T10:30:54.000Z",
            "amount": 1000,
            "charged_amount": 1000,
            "status": "successful",
            "IP": "52.209.154.143",
            "currency": "USD",
            "appfee": 38,
            "merchantfee": 0,
            "merchantbearsfee": 1,
            "customer": {
                "id": 1475197,
                "phone": None,
                "fullName": "adewale bolu",
                "customertoken": None,
                "email": "test@gmail.com",
                "createdAt": "2021-12-24T10:30:54.000Z",
                "updatedAt": "2021-12-24T10:30:54.000Z",
                "deletedAt": None,
                "AccountId": 87881
            },
            "entity": {
                "card6": "424242",
                "card_last4": "4242",
                "card_country_iso": "US",
                "createdAt": "2017-02-27T17:33:38.000Z"
            },
            "event.type": "CARD_TRANSACTION"
        }

FLUTTERWAVE_PAYMENT_VERIFY_RESPONSE = {"status":"success","message":"Transaction fetched successfully","data":{"id":2767577,"tx_ref":"69c7a6a1-97e0-49c3-a4b7-483260d816da","flw_ref":"FLW-MOCK-3aa480ac93a46883f384d63eb8485796","device_fingerprint":"80f56d7f5f16927f91485431588e0d79","amount":1000,"currency":"USD","charged_amount":1000,"app_fee":38,"merchant_fee":0,"processor_response":"Approved. Successful","auth_model":"VBVSECURECODE","ip":"52.209.154.143","narration":"CARD Transaction ","status":"successful","payment_type":"card","created_at":"2021-12-24T10:30:54.000Z","account_id":87881,"card":{"first_6digits":"424242","last_4digits":"4242","issuer":" CREDIT","country":"VISA TEST CARD","type":"VISA","token":"flw-t1nf-13d646bc7403806ac219a2f48eb9b7ca-m03k","expiry":"09/20"},"meta":{"__CheckoutInitAddress":"https://ravemodal-dev.herokuapp.com/v3/hosted/pay/4065b68a6657c93cd11d","user_id":"8ca7237d-346e-4cd5-9149-9d15339c13c7"},"plan":16614,"amount_settled":962,"customer":{"id":1475197,"name":"adewale bolu","phone_number":"N/A","email":"test@gmail.com","created_at":"2021-12-24T10:30:54.000Z"}}}
# Create your tests here.
STRIPE_CREATE_CUSTOMER_RESPONSE = '''{
  "account_balance": 0,
  "address": null,
  "balance": 0,
  "created": 1640434693,
  "currency": null,
  "default_source": null,
  "delinquent": false,
  "description": null,
  "discount": null,
  "email": "test@gmail.com",
  "id": "cus_KqFhUAVg4wYfZm",
  "invoice_prefix": "47B8770D",
  "invoice_settings": {
    "custom_fields": null,
    "default_payment_method": null,
    "footer": null
  },
  "livemode": false,
  "metadata": {},
  "name": null,
  "next_invoice_sequence": 1,
  "object": "customer",
  "phone": null,
  "preferred_locales": [],
  "shipping": null,
  "sources": {
    "data": [],
    "has_more": false,
    "object": "list",
    "total_count": 0,
    "url": "/v1/customers/cus_KqFhUAVg4wYfZm/sources"
  },
  "subscriptions": {
    "data": [],
    "has_more": false,
    "object": "list",
    "total_count": 0,
    "url": "/v1/customers/cus_KqFhUAVg4wYfZm/subscriptions"
  },
  "tax_exempt": "none",
  "tax_ids": {
    "data": [],
    "has_more": false,
    "object": "list",
    "total_count": 0,
    "url": "/v1/customers/cus_KqFhUAVg4wYfZm/tax_ids"
  },
  "tax_info": null,
  "tax_info_verification": null
}'''

def create_test_user(user_type):
    return User.objects.create(email="test@gmail.com", full_name='adewale bolu', user_type=user_type)

def create_test_doctor():
    return DoctorInfo.objects.create(user=create_test_user(UserType.DOCTOR), username='aa')

def create_test_clinic():
    return ClinicInfo.objects.create(user=create_test_user(UserType.CLINIC), username='aa')

def create_test_pharmacy():
    return PharmacyInfo.objects.create(user=create_test_user(UserType.PHARMACY), username='aa')


class SubscriptionSerializerTestCase(TestCase):
    def test_get_object_with_doctor(self):
        doctor = create_test_doctor()
        serializer = SubscriptionSerializer(data={'account_type': UserType.DOCTOR, 'account_id': doctor.id})
        serializer.is_valid(raise_exception=True)
        obj = serializer.get_object()
        self.assertEqual(obj, doctor)

    def test_get_object_with_clinic(self):
        doctor = create_test_clinic()
        serializer = SubscriptionSerializer(data={'account_type': UserType.CLINIC, 'account_id': doctor.id})
        serializer.is_valid(raise_exception=True)
        obj = serializer.get_object()
        self.assertEqual(obj, doctor)

    def test_get_object_with_pharmacy(self):
        doctor = create_test_pharmacy()
        serializer = SubscriptionSerializer(data={'account_type': UserType.PHARMACY, 'account_id': doctor.id})
        serializer.is_valid(raise_exception=True)
        obj = serializer.get_object()
        self.assertEqual(obj, doctor)

    def test_not_accepting_non_subscription_types(self):
        doctor = create_test_pharmacy()
        serializer = SubscriptionSerializer(data={'account_type': UserType.PATIENT, 'account_id': doctor.id})
        pp = serializer.is_valid()
        self.assertEqual(pp, False)


class FluterwaveProviderTest(TestCase):
    def test_create_subscription(self):
        provider = FluterwaveProviver()
        # res = provider.init_subscription(create_test_user(UserType.DOCTOR), 1000) #(16610, 'https://ravemodal-dev.herokuapp.com/v3/hosted/pay/4a3a6518413ccac515b0')
        # print(res)
    
    def _test_flutterwave_webhook(self):

        headers = {
            'verif-hash': 'hhhhhhhhhhhhhhhhhhhh'
        }
        res = self.client.post(path='/subscription/flutterwave-webhook', json=FLUTTERWAVE_WEBHOOK_PAYLOAD, headers=headers)
        print(res, "jj")

    def test_flutterwave_provider_webhook(self):
        request = Mock(headers={'verif-hash': 'sssssss'}, data=FLUTTERWAVE_WEBHOOK_PAYLOAD)
        FluterwaveProviver().handle_webhook(request)
        # TODO: Confirm the test


class StripeProviderTest(TestCase):
    def test_create_stripe_subscription(self):
        card = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 12,
                "exp_year": 2022,
                "cvc": "314",
            },
        )
        # payment_method_id = "pm_1KAZ7I2eZvKYlo2CmwHofzLP"
        payment_method_id = card.id
        provider = StripeProvider()
        provider.create_subscription(create_test_user(UserType.DOCTOR), 1, payment_method_id, 'price_1KAYc9DHO41eP91MMM7OIo4t')
        print(kk)

class PayPalAPITest(TestCase):
    def test_auth(self):
        # api = PayPalAPI().authenticate()
        create_paypal_plan()
        
