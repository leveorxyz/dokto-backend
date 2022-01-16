import json
from unittest.mock import Mock, patch
from django.test import TestCase
from django.urls import reverse
from subscription.mixins import UserType
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider, SubscriptionType
from subscription.providers import FluterwaveProviver, PaypalProvider, PaystackProvider, Provider, StripeProvider, stripe
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

STRIPE_CREATE_SUBSCRIPTION_RESPONSE = '''{
  "application_fee_percent": null,
  "automatic_tax": {
    "enabled": false
  },
  "billing": "charge_automatically",
  "billing_cycle_anchor": 1640529100,
  "billing_thresholds": null,
  "cancel_at": null,
  "cancel_at_period_end": false,
  "canceled_at": null,
  "collection_method": "charge_automatically",
  "created": 1640529100,
  "current_period_end": 1643207500,
  "current_period_start": 1640529100,
  "customer": "cus_Kqf5DEolBv0PXG",
  "days_until_due": null,
  "default_payment_method": null,
  "default_source": null,
  "default_tax_rates": [],
  "discount": null,
  "ended_at": null,
  "id": "sub_1KAxlADHO41eP91Mkwsiltso",
  "invoice_customer_balance_settings": {
    "consume_applied_balance_on_void": true
  },
  "items": {
    "data": [
      {
        "billing_thresholds": null,
        "created": 1640529101,
        "id": "si_Kqf5c92BbjS9zg",
        "metadata": {},
        "object": "subscription_item",
        "plan": {
          "active": true,
          "aggregate_usage": null,
          "amount": 5000,
          "amount_decimal": "5000",
          "billing_scheme": "per_unit",
          "created": 1640432441,
          "currency": "usd",
          "id": "price_1KAYc9DHO41eP91MMM7OIo4t",
          "interval": "month",
          "interval_count": 1,
          "livemode": false,
          "metadata": {},
          "nickname": null,
          "object": "plan",
          "product": "prod_KqF6chMhR95psS",
          "tiers": null,
          "tiers_mode": null,
          "transform_usage": null,
          "trial_period_days": null,
          "usage_type": "licensed"
        },
        "price": {
          "active": true,
          "billing_scheme": "per_unit",
          "created": 1640432441,
          "currency": "usd",
          "id": "price_1KAYc9DHO41eP91MMM7OIo4t",
          "livemode": false,
          "lookup_key": null,
          "metadata": {},
          "nickname": null,
          "object": "price",
          "product": "prod_KqF6chMhR95psS",
          "recurring": {
            "aggregate_usage": null,
            "interval": "month",
            "interval_count": 1,
            "trial_period_days": null,
            "usage_type": "licensed"
          },
          "tax_behavior": "unspecified",
          "tiers_mode": null,
          "transform_quantity": null,
          "type": "recurring",
          "unit_amount": 5000,
          "unit_amount_decimal": "5000"
        },
        "quantity": 1,
        "subscription": "sub_1KAxlADHO41eP91Mkwsiltso",
        "tax_rates": []
      }
    ],
    "has_more": false,
    "object": "list",
    "total_count": 1,
    "url": "/v1/subscription_items?subscription=sub_1KAxlADHO41eP91Mkwsiltso"
  },
  "latest_invoice": "in_1KAxlADHO41eP91M3idhU2Ja",
  "livemode": false,
  "metadata": {},
  "next_pending_invoice_item_invoice": null,
  "object": "subscription",
  "pause_collection": null,
  "payment_settings": {
    "payment_method_options": null,
    "payment_method_types": null
  },
  "pending_invoice_item_interval": null,
  "pending_setup_intent": null,
  "pending_update": null,
  "plan": {
    "active": true,
    "aggregate_usage": null,
    "amount": 5000,
    "amount_decimal": "5000",
    "billing_scheme": "per_unit",
    "created": 1640432441,
    "currency": "usd",
    "id": "price_1KAYc9DHO41eP91MMM7OIo4t",
    "interval": "month",
    "interval_count": 1,
    "livemode": false,
    "metadata": {},
    "nickname": null,
    "object": "plan",
    "product": "prod_KqF6chMhR95psS",
    "tiers": null,
    "tiers_mode": null,
    "transform_usage": null,
    "trial_period_days": null,
    "usage_type": "licensed"
  },
  "quantity": 1,
  "schedule": null,
  "start": 1640529100,
  "start_date": 1640529100,
  "status": "active",
  "tax_percent": null,
  "transfer_data": null,
  "trial_end": null,
  "trial_start": null
}'''

STRIPE_CREATE_SUBSCRIPTION_WEBHOOK = '''{
  "id": "evt_1KAxlDDHO41eP91MJAqN6LnO",
  "object": "event",
  "api_version": "2019-03-14",
  "created": 1640529102,
  "data": {
    "object": {
      "id": "sub_1KAxlADHO41eP91Mkwsiltso",
      "object": "subscription",
      "application_fee_percent": null,
      "automatic_tax": {
        "enabled": false
      },
      "billing": "charge_automatically",
      "billing_cycle_anchor": 1640529100,
      "billing_thresholds": null,
      "cancel_at": null,
      "cancel_at_period_end": false,
      "canceled_at": null,
      "collection_method": "charge_automatically",
      "created": 1640529100,
      "current_period_end": 1643207500,
      "current_period_start": 1640529100,
      "customer": "cus_Kqf5DEolBv0PXG",
      "days_until_due": null,
      "default_payment_method": null,
      "default_source": null,
      "default_tax_rates": [],
      "discount": null,
      "ended_at": null,
      "invoice_customer_balance_settings": {
        "consume_applied_balance_on_void": true
      },
      "items": {
        "object": "list",
        "data": [
          {
            "id": "si_Kqf5c92BbjS9zg",
            "object": "subscription_item",
            "billing_thresholds": null,
            "created": 1640529101,
            "metadata": {},
            "plan": {
              "id": "price_1KAYc9DHO41eP91MMM7OIo4t",
              "object": "plan",
              "active": true,
              "aggregate_usage": null,
              "amount": 5000,
              "amount_decimal": "5000",
              "billing_scheme": "per_unit",
              "created": 1640432441,
              "currency": "usd",
              "interval": "month",
              "interval_count": 1,
              "livemode": false,
              "metadata": {},
              "nickname": null,
              "product": "prod_KqF6chMhR95psS",
              "tiers": null,
              "tiers_mode": null,
              "transform_usage": null,
              "trial_period_days": null,
              "usage_type": "licensed"
            },
            "price": {
              "id": "price_1KAYc9DHO41eP91MMM7OIo4t",
              "object": "price",
              "active": true,
              "billing_scheme": "per_unit",
              "created": 1640432441,
              "currency": "usd",
              "livemode": false,
              "lookup_key": null,
              "metadata": {},
              "nickname": null,
              "product": "prod_KqF6chMhR95psS",
              "recurring": {
                "aggregate_usage": null,
                "interval": "month",
                "interval_count": 1,
                "trial_period_days": null,
                "usage_type": "licensed"
              },
              "tax_behavior": "unspecified",
              "tiers_mode": null,
              "transform_quantity": null,
              "type": "recurring",
              "unit_amount": 5000,
              "unit_amount_decimal": "5000"
            },
            "quantity": 1,
            "subscription": "sub_1KAxlADHO41eP91Mkwsiltso",
            "tax_rates": []
          }
        ],
        "has_more": false,
        "total_count": 1,
        "url": "/v1/subscription_items?subscription=sub_1KAxlADHO41eP91Mkwsiltso"
      },
      "latest_invoice": "in_1KAxlADHO41eP91M3idhU2Ja",
      "livemode": false,
      "metadata": {},
      "next_pending_invoice_item_invoice": null,
      "pause_collection": null,
      "payment_settings": {
        "payment_method_options": null,
        "payment_method_types": null
      },
      "pending_invoice_item_interval": null,
      "pending_setup_intent": null,
      "pending_update": null,
      "plan": {
        "id": "price_1KAYc9DHO41eP91MMM7OIo4t",
        "object": "plan",
        "active": true,
        "aggregate_usage": null,
        "amount": 5000,
        "amount_decimal": "5000",
        "billing_scheme": "per_unit",
        "created": 1640432441,
        "currency": "usd",
        "interval": "month",
        "interval_count": 1,
        "livemode": false,
        "metadata": {},
        "nickname": null,
        "product": "prod_KqF6chMhR95psS",
        "tiers": null,
        "tiers_mode": null,
        "transform_usage": null,
        "trial_period_days": null,
        "usage_type": "licensed"
      },
      "quantity": 1,
      "schedule": null,
      "start": 1640529100,
      "start_date": 1640529100,
      "status": "active",
      "tax_percent": null,
      "transfer_data": null,
      "trial_end": null,
      "trial_start": null
    }
  },
  "livemode": false,
  "pending_webhooks": 4,
  "request": {
    "id": "req_CW8dLdk4TWykGY",
    "idempotency_key": "12d5751d-6ea6-4cd9-b028-9e78588ba2f6"
  },
  "type": "customer.subscription.created"
}'''

PAYSTACK_CREATE_SUBSCRIPTION_WEBHOOK = '''{"event":"subscription.create","data":{"id":342134,"domain":"test","status":"active","subscription_code":"SUB_xzi8h2b2gh4kteh","email_token":"kcrdisxm28kkqnn","amount":10000,"cron_expression":"0 0 26 * *","next_payment_date":"2022-01-26T00:00:00.000Z","open_invoice":null,"cancelledAt":null,"integration":340657,"plan":{"id":209655,"name":"Monthly Retainer","plan_code":"PLN_dgmhppri4ugfv6u","description":null,"amount":10000,"interval":"monthly","send_invoices":true,"send_sms":true,"currency":"NGN"},"authorization":{"authorization_code":"AUTH_n1p1c0sr0h","bin":"408408","last4":"4081","exp_month":"12","exp_year":"2030","channel":"card","card_type":"visa ","bank":"TEST BANK","country_code":"NG","brand":"visa","reusable":true,"signature":"SIG_4ZcqUoUO3vOMZqk9r9VL","account_name":null},"customer":{"id":65484192,"first_name":null,"last_name":null,"email":"customer@email.com","customer_code":"CUS_1q72l1li3tim90m","phone":null,"metadata":null,"risk_action":"default","international_format_phone":null},"invoices":[],"invoices_history":[],"invoice_limit":0,"split_code":null,"most_recent_invoice":null,"created_at":"2021-12-26T16:08:16.000Z"}}'''
PAYPAL_CREATE_SUBSCRIPTION_WEBHOOK = '''{"id":"WH-33353026SL686772R-3EJ77569F56872828","event_version":"1.0","create_time":"2021-12-26T19:56:41.498Z","resource_type":"subscription","resource_version":"2.0","event_type":"BILLING.SUBSCRIPTION.ACTIVATED","summary":"Subscription activated","resource":{"quantity":"1","subscriber":{"email_address":"reedon.ne@gmail.com","payer_id":"B26HDHPTNL4JC","name":{"given_name":"buyer","surname":"one"},"shipping_address":{"name":{"full_name":"adewale bolu"},"address":{"address_line_1":"2211 N First Street","address_line_2":"Building 17","admin_area_2":"San Jose","admin_area_1":"CA","postal_code":"95131","country_code":"US"}}},"create_time":"2021-12-26T19:56:25Z","plan_overridden":false,"shipping_amount":{"currency_code":"USD","value":"0.0"},"start_time":"2021-12-27T15:57:47Z","update_time":"2021-12-26T19:56:27Z","billing_info":{"outstanding_balance":{"currency_code":"USD","value":"0.0"},"cycle_executions":[{"tenure_type":"TRIAL","sequence":1,"cycles_completed":0,"cycles_remaining":2,"current_pricing_scheme_version":1,"total_cycles":2},{"tenure_type":"TRIAL","sequence":2,"cycles_completed":0,"cycles_remaining":3,"current_pricing_scheme_version":1,"total_cycles":3},{"tenure_type":"REGULAR","sequence":3,"cycles_completed":0,"cycles_remaining":12,"current_pricing_scheme_version":1,"total_cycles":12}],"last_payment":{"amount":{"currency_code":"USD","value":"11.0"},"time":"2021-12-26T19:56:26Z"},"next_billing_time":"2021-12-27T10:00:00Z","final_payment_time":"2023-04-27T10:00:00Z","failed_payments_count":0},"links":[{"href":"https://api.sandbox.paypal.com/v1/billing/subscriptions/I-P321C4J8V4S7/cancel","rel":"cancel","method":"POST","encType":"application/json"},{"href":"https://api.sandbox.paypal.com/v1/billing/subscriptions/I-P321C4J8V4S7","rel":"edit","method":"PATCH","encType":"application/json"},{"href":"https://api.sandbox.paypal.com/v1/billing/subscriptions/I-P321C4J8V4S7","rel":"self","method":"GET","encType":"application/json"},{"href":"https://api.sandbox.paypal.com/v1/billing/subscriptions/I-P321C4J8V4S7/suspend","rel":"suspend","method":"POST","encType":"application/json"},{"href":"https://api.sandbox.paypal.com/v1/billing/subscriptions/I-P321C4J8V4S7/capture","rel":"capture","method":"POST","encType":"application/json"}],"id":"I-P321C4J8V4S7","plan_id":"P-65B87060MP233174UMHEMDHA","auto_renewal":false,"status":"ACTIVE","status_update_time":"2021-12-26T19:56:27Z"},"links":[{"href":"https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-33353026SL686772R-3EJ77569F56872828","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-33353026SL686772R-3EJ77569F56872828/resend","rel":"resend","method":"POST"}]}'''

def create_test_user(user_type=UserType.DOCTOR):
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
        provider = StripeProvider()
        provider.create_subscription(create_test_user(UserType.DOCTOR), 1, 'tok_visa', 'price_1KAYc9DHO41eP91MMM7OIo4t')

class PayPalAPITest(TestCase):
    def test_auth(self):
        # api = PayPalAPI().authenticate()
        create_paypal_plan('doctor', 10000)


class PayPalProviderTest(TestCase):
    def test_create_subscription(self):
        plan_id = 'P-65B87060MP233174UMHEMDHA'
        provider = PaypalProvider()
        res = provider.init_subscription(create_test_user(UserType.DOCTOR), 1, plan_id)
        print(res)

    def test_paypal_webhook(self):
        url = reverse('subscription:paypal-webhook')
        headers = {
        }
        
        SubscriptionHistory.objects.create(payment_method=SubscriptionPaymantProvider.PAYPAL, payment_ref='I-P321C4J8V4S7', user=create_test_user(),)
        res = self.client.post(url, PAYPAL_CREATE_SUBSCRIPTION_WEBHOOK, content_type="application/json", **headers)
        print(res)
        

class PaystackProviderTest(TestCase):
    def test_create_subscription(self):
        provider = PaystackProvider()
        res = provider.init_subscription(create_test_user(UserType.DOCTOR), 10000)
        print(res)
    
    def test_paystack_webhook(self):
        url = reverse('subscription:paystack-webhook')
        headers = {
            'HTTP_x-paystack-signature': '1a7c2eefd224fb0bcd19cf2dc4d37330917bdfbd7585a63ecc6cf1018f3bd1dfcea4601a96954c3254cd086c63c012b28083629da610db4de519de7f8507d4d5',
            'Content-Type': 'application/json'
        }
        
        SubscriptionHistory.objects.create(payment_method=SubscriptionPaymantProvider.PAYSTACK, payment_ref='PLN_dgmhppri4ugfv6u', user=create_test_user(),)
        res = self.client.post(url, PAYSTACK_CREATE_SUBSCRIPTION_WEBHOOK, content_type="application/json", **headers)
