from datetime import datetime, timedelta
import requests
from requests.models import HTTPBasicAuth
from django.conf import settings
from gateways.gateway import Gateway
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider, SubscriptionPlanTypes

from user.models import User


PAYPAL_SUBSCRIPTION_RETURN_URL = 'https://example.com/' # TODO: Collect from frontend
PAYPAL_SUBSCRIPTION_CANCEL_URL = 'https://example.com/' # TODO: Collect from frontend

PAYPAL_PLAN_T0_PLAN_ID_CONVERSION_DICT = {
    SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE: settings.PAYPAL_DOTOR_SUSBCRIPTION_PRICE,
    SubscriptionPlanTypes.PHARMACY_SUBSCRIPTION_PLAN: settings.PAYPAL_PHARMACY_SUBSCRIPTION_PRICE,
    SubscriptionPlanTypes.CLINIC_SUBSCRIPTION_PLAN: settings.PAYPAL_CLINIC_SUBSCRIPTION_PRICE,
    SubscriptionPlanTypes.DOCTOR_WITH_HOME_SERVICE: settings.PAYPAL_DOCTOR_WITH_HOME_SERVICE_PRICE,
}


class PaypalEventTypes:
    SUBSCRIPTION_CREATED = 'BILLING.SUBSCRIPTION.ACTIVATED'
    SUBSCRIPTION_UPDATED = 'BILLING.SUBSCRIPTION.UPDATED'
    SUBSCRIPTION_RENEWED = 'BILLING.SUBSCRIPTION.RENEWED'
    
    all = [SUBSCRIPTION_CREATED, SUBSCRIPTION_UPDATED, SUBSCRIPTION_RENEWED]


PAYPAL_API_TEST_BASE_URL = 'https://api-m.sandbox.paypal.com/v1/'
PAYPAL_API_LIVE_BASE_URL = 'https://api-m.paypal.com'
PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET = settings.PAYPAL_CLIENT_SECRET

class PayPalAPI(Gateway):
    def __init__(self):
        self.paypal_token = None
        self.PAYPAL_API_BASE_URL = PAYPAL_API_TEST_BASE_URL if settings.DEBUG else PAYPAL_API_LIVE_BASE_URL

    def authenticate(self):
        response = requests.post(self.PAYPAL_API_BASE_URL + 'oauth2/token', data={
            'grant_type': 'client_credentials'
        }, auth=HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET))
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        access_token = response_dict['access_token']
        expires_in = response_dict['expires_in']
        return access_token, expires_in

    def send(self, path, method, params={}, json={}):
        if not self.paypal_token:
            token, _ = self.authenticate() # TODO: Save token in cache
            self.paypal_token = token
        headers = {'Authorization': f'Bearer {self.paypal_token}'}
        print(headers)
        response = requests.request(method, self.PAYPAL_API_BASE_URL + path, params=params, json=json, headers=headers)
        if response.status_code not in [200, 201, 204]:
            print(response.content)
            raise Exception()
        return response
    
    def create_billing_plan(self, data):
        return self.send('billing/plans', 'POST', {}, data)

    def create_billing_product(self, data):
        return self.send('catalogs/products', 'POST', {}, data)


class PaypalProvider():

    def get_provider_type(self):
        return SubscriptionPaymantProvider.PAYPAL

    def init_subscription(self, user: User, no_of_doctors: int, paypal_plan_id: str):
        response = PayPalAPI().send('billing/subscriptions', "POST", json={
            'plan_id': paypal_plan_id,
            'start_time': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'quantity': no_of_doctors,
            'subscriber': {
                'name': {
                'given_name': user.first_name,
                'surname': user.last_name
                },
                'email_address': user.email,
                'shipping_address': {
                    'name': {
                        'full_name': user.full_name
                    },
                    'address': {
                        'country_code': 'US' # TODO: CHange to user country
                    }
                }
            },
            'application_context': {
                'brand_name': 'DOKITA',
                'locale': 'en-US',
                'user_action': 'SUBSCRIBE_NOW',
                'payment_method': {
                    'payee_preferred': 'IMMEDIATE_PAYMENT_REQUIRED'
                },
                'return_url': PAYPAL_SUBSCRIPTION_RETURN_URL,
                'cancel_url': PAYPAL_SUBSCRIPTION_CANCEL_URL
            }
        })

        status = response.json()['status']
        if status != 'APPROVAL_PENDING':
            raise Exception()
        response_json = response.json()
        sub_id = response_json['id']
        links = response_json['links']
        approval_url = None
        for link in links:
            if link['rel'] == 'approve':
                approval_url = link['href']
        if not approval_url:
            raise Exception()
        return sub_id, approval_url

    def _cancel_subscription(self, subscription: SubscriptionHistory):
        path = f'billing/subscriptions/{subscription.payment_ref}/cancel'
        response = PayPalAPI().send('billing/subscriptions', "POST", json={
            'reason': 'Reason' # TODO: Q: Should we collect reason from user?
        })

    def _verify_webhook(self, request):
        # TODO: Implement webhook verification
        return True

    def _handle_webhook(self, data):
        event_type = data['event_type']
        print(event_type)
        if event_type not in PaypalEventTypes.all:
            return
        obj = data['resource']
        subscription_id = obj['id']
        status = obj['status']
        if status != 'ACTIVE':
            return
        start_time_string = obj['billing_info']['last_payment']['time'] # No payment ID from paypal but payment time can 
                                                                        # also uniquely identify a subscription payment
        start_time = datetime.strptime(start_time_string, '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.strptime(obj['billing_info']['next_billing_time'], '%Y-%m-%dT%H:%M:%SZ')
        return subscription_id, start_time_string, start_time, end_time

    def _subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        return self.init_subscription(user, quantity, PAYPAL_PLAN_T0_PLAN_ID_CONVERSION_DICT.get(plan_type))
