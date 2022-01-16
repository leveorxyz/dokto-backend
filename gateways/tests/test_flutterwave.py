import json
from unittest.mock import patch, Mock
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from gateways.flutterwave import FluterwaveProviver, FlutterwaveAPI
from gateways.paypal import PaypalProvider

from .test_gateway import create_test_user


TEST_PLAN_ID = 16729
TEST_AMOUNT = 10000
TEST_PAYMENT_LINK = 'https://ravemodal-dev.herokuapp.com/v3/hosted/pay/a16b34804faa3eb5bc1f'
TEST_CREATE_PLAN_RESPONSE = {'status': 'success', 'message': 'Payment plan created', 'data': {'id': TEST_PLAN_ID, 'name': 'Dokita Plan', 'amount': TEST_AMOUNT / 100, 'interval': 'Monthly', 'duration': 0, 'status': 'active', 'currency': 'USD', 'plan_token': 'rpp_5ddc14acb131c20a7c4f', 'created_at': '2021-12-28T17:54:36.000Z'}}
TEST_CREATE_SUBSCRIPTION = {'status': 'success', 'message': 'Hosted Link', 'data': {'link': TEST_PAYMENT_LINK}}
CHARGE_SUBSCRIPTION_WEBHOOK = '''{"id":2782409,"txRef":"077d6e38-1b89-4108-a154-8d284f89d30f","flwRef":"FLW-M03K-01d1aa68ea3fec36f2b6cfa589b9e122","orderRef":"URF_9D8CAA96CD6DFDED9E_9049056","paymentPlan":16733,"paymentPage":null,"createdAt":"2021-12-28T19:17:29.000Z","amount":100,"charged_amount":100,"status":"successful","IP":"52.209.154.143","currency":"USD","appfee":3.8,"merchantfee":0,"merchantbearsfee":1,"customer":{"id":1477959,"phone":"07032935357","fullName":"name last","customertoken":null,"email":"test@test.com","createdAt":"2021-12-28T18:27:45.000Z","updatedAt":"2021-12-28T18:27:45.000Z","deletedAt":null,"AccountId":87881},"entity":{"card6":"424242","card_last4":"4242","card_country_iso":"US","createdAt":"2017-02-27T17:33:38.000Z"},"event.type":"CARD_TRANSACTION"}'''

class FlutterwaveTest(TestCase):

    @patch('gateways.flutterwave.FlutterwaveAPI.request', return_value=TEST_CREATE_PLAN_RESPONSE)
    def test_create_plan(self, _mock_api):
        api = FlutterwaveAPI()
        provider = FluterwaveProviver()
        plan_id = provider._create_plan(api, TEST_AMOUNT)
        self.assertEqual(plan_id, TEST_PLAN_ID)

    @patch('gateways.flutterwave.FlutterwaveAPI.request', return_value=TEST_CREATE_SUBSCRIPTION)
    def test_create_subscription(self, _mock_api):
        api = FlutterwaveAPI()
        provider = FluterwaveProviver()
        id, approval_url = provider._create_subscription(api, create_test_user(), TEST_PLAN_ID, TEST_AMOUNT)
        self.assertEqual(approval_url, TEST_PAYMENT_LINK)

    def test_verify_webhook(self):
        request = Mock(body=CHARGE_SUBSCRIPTION_WEBHOOK.encode('utf-8'), headers={
            'Verif-Hash': 'hhhhhhhhhhhhhhhhhhhh'
        })
        
        # Test with correct secret key
        with self.settings(FLUTTERWAVE_WEBHOOK_VERIFICATION_HASH='hhhhhhhhhhhhhhhhhhhh'):
            FluterwaveProviver()._verify_webhook(request)
            self.assertTrue(True)

        # Test with wrong secret key
        with self.settings(FLUTTERWAVE_WEBHOOK_VERIFICATION_HASH='wrong-key'):
            self.assertRaises(AuthenticationFailed, lambda: FluterwaveProviver()._verify_webhook(request))

    def test_webhook(self):
        payment_ref, payment_id, start_time, end_time = FluterwaveProviver()._handle_webhook(json.loads(CHARGE_SUBSCRIPTION_WEBHOOK))
        print(payment_ref, payment_id, start_time, end_time)

