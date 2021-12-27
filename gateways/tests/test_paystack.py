import json
from unittest.mock import patch, Mock
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied

from gateways.paystack import PaystackAPI, PaystackProvider


TEST_PLAN_CODE = 'PLN_u4swzrr7rl8l2ws'
TEST_SUBSCRIPTION_PRICE = 100000
CREATE_PLAN_RESPONSE = {'status': True, 'message': 'Plan created', 'data': {'name': 'Monthly Retainer', 'interval': 'monthly', 'amount': TEST_SUBSCRIPTION_PRICE, 'integration': 340657, 'domain': 'test', 'currency': 'NGN', 'plan_code': 'PLN_u4swzrr7rl8l2ws', 'invoice_limit': 0, 'send_invoices': True, 'send_sms': True, 'hosted_page': False, 'migrate': False, 'is_archived': False, 'id': 209779, 'createdAt': '2021-12-28T14:06:33.886Z', 'updatedAt': '2021-12-28T14:06:33.886Z'}}
CREATE_SUBSCRIPTION_RESPONSE = {'status': True, 'message': 'Authorization URL created', 'data': {'authorization_url': 'https://checkout.paystack.com/tqpkeu7mxrzup0g', 'access_code': 'tqpkeu7mxrzup0g', 'reference': 'nqotuzvaur'}}
CREATE_SUBSCRIPTION_WEBHOOK = '''{"event":"subscription.create","data":{"id":342389,"domain":"test","status":"active","subscription_code":"SUB_xp7t7c9371s86m2","email_token":"vbm14vhy7pe2qte","amount":100000,"cron_expression":"0 0 28 * *","next_payment_date":"2022-01-28T00:00:00.000Z","open_invoice":null,"cancelledAt":null,"integration":340657,"plan":{"id":209779,"name":"Monthly Retainer","plan_code":"PLN_u4swzrr7rl8l2ws","description":null,"amount":100000,"interval":"monthly","send_invoices":true,"send_sms":true,"currency":"NGN"},"authorization":{"authorization_code":"AUTH_u05bcj3dic","bin":"408408","last4":"4081","exp_month":"12","exp_year":"2030","channel":"card","card_type":"visa ","bank":"TEST BANK","country_code":"NG","brand":"visa","reusable":true,"signature":"SIG_4ZcqUoUO3vOMZqk9r9VL","account_name":null},"customer":{"id":65484192,"first_name":null,"last_name":null,"email":"customer@email.com","customer_code":"CUS_1q72l1li3tim90m","phone":null,"metadata":null,"risk_action":"default","international_format_phone":null},"invoices":[],"invoices_history":[],"invoice_limit":0,"split_code":null,"most_recent_invoice":null,"created_at":"2021-12-28T14:26:37.000Z"}}'''
CHARGE_SUCCESS_WEBHOOK = '''{
  "event": "charge.success",
  "data": {
    "id": 84,
    "domain": "test",
    "status": "success",
    "reference": "9cfbae6e-bbf3-5b41-8aef-d72c1a17650g",
    "amount": 50000,
    "message": null,
    "gateway_response": "Approved",
    "paid_at": "2018-12-20T15:00:06.000Z",
    "created_at": "2018-12-20T15:00:05.000Z",
    "channel": "card",
    "currency": "NGN",
    "ip_address": null,
    "metadata": {
      "custom_fields": [
        {
          "display_name": "A sample",
          "variable_name": "a_sample",
          "value": "custom field"
        }
      ]
    },
    "log": null,
    "fees": 750,
    "fees_split": null,
    "authorization": {
      "authorization_code": "AUTH_9246d0h9kl",
      "bin": "408408",
      "last4": "4081",
      "exp_month": "12",
      "exp_year": "2020",
      "channel": "card",
      "card_type": "visa DEBIT",
      "bank": "Test Bank",
      "country_code": "NG",
      "brand": "visa",
      "reusable": true,
      "signature": "SIG_iCw3p0rsG7LUiQwlsR3t"
    },
    "customer": {
      "id": 4670376,
      "first_name": "Asample",
      "last_name": "Personpaying",
      "email": "asam@ple.com",
      "customer_code": "CUS_00w4ath3e2ukno4",
      "phone": "",
      "metadata": null,
      "risk_action": "default"
    },
    "plan": {
      "id": 17,
      "name": "A s(i/a)mple plan",
      "plan_code": "PLN_dbam2fwcqkyyfjc",
      "description": "Sample plan for docs",
      "amount": 50000,
      "interval": "hourly",
      "send_invoices": true,
      "send_sms": true,
      "currency": "NGN"
    },
    "subaccount": {},
    "paidAt": "2018-12-20T15:00:06.000Z"
  }
}'''

class PaystackTest(TestCase):

    @patch('gateways.paystack.PaystackAPI.post')
    def test_create_plan(self, mock_api_call):
        mock_api_call.return_value = Mock(**{
            'json.return_value': CREATE_PLAN_RESPONSE
        })
        api = PaystackAPI()
        provider = PaystackProvider()
        plan_code = provider._create_plan(api, TEST_SUBSCRIPTION_PRICE)
        self.assertEqual(plan_code, TEST_PLAN_CODE)

    @patch('gateways.paystack.PaystackAPI.post')
    def test_init_subscription(self, mock_api_call):
        mock_api_call.return_value = Mock(**{
            'json.return_value': CREATE_SUBSCRIPTION_RESPONSE
        })
        api = PaystackAPI()
        provider = PaystackProvider()
        plan_code, auth_url = provider._initialize_subscription(api, TEST_SUBSCRIPTION_PRICE, TEST_PLAN_CODE)
        self.assertEqual(plan_code, TEST_PLAN_CODE)
        self.assertEqual(auth_url, 'https://checkout.paystack.com/tqpkeu7mxrzup0g')

    def test_verify_webhook(self):
        request = Mock(headers={
            'X-Paystack-Signature': 'c4522de7a85dc5c910b54b80ae5b0bf22e18f043961409459d11052814d6283ea9ba0610da25c62cd0dcba6a00b5ab7cee120768f09f669a55221f335ed4abed',
        }, data=json.loads(CREATE_SUBSCRIPTION_WEBHOOK), body=CREATE_SUBSCRIPTION_WEBHOOK.encode('utf-8'))
        # Test with correct secret key
        with self.settings(PAYSTACK_SECRET_KEY='sk_test_b8fdadbb4426e37276abdf0a28528b4085ddb4a9'):
            PaystackProvider()._verify_webhook(request)
            self.assertTrue(True)

        # Test with wrong secret key
        with self.settings(PAYSTACK_SECRET_KEY='wrong-key'):
            self.assertRaises(PermissionDenied, lambda: PaystackProvider()._verify_webhook(request))

    def test_create_subscription_webhook(self):
        payment_ref, new_payment_id, start_time, end_time = PaystackProvider()._handle_webhook(json.loads(CREATE_SUBSCRIPTION_WEBHOOK))
        self.assertEqual(payment_ref, TEST_PLAN_CODE)
        self.assertEqual(new_payment_id)
        # TODO: Wait till test subscriptions to charge for the second day by 16:14 on 28-Dec to confirm behaviour
