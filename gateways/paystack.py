from datetime import datetime, time, timedelta
import hashlib
import hmac
from re import sub
import requests
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from stripe.api_resources import subscription
from gateways.gateway import Gateway
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider

from user.models import User

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY


class PaystackEventType:
    SUBSCRIPTION_CREATED = 'subscription.create'
    all = [SUBSCRIPTION_CREATED]


class PaystackAPI():

    def post(self, path, json={}):
        res = requests.post("https://api.paystack.co/" + path, json=json, headers={
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
        })
        if res.status_code not in [200, 201]:
            raise Exception()
        return res


EXTRA_SUBSCRIPTION_FIELD_SPLITTER = '|'

def _get_extra_subscription_field(subscription_code, email_token):
    return subscription_code + EXTRA_SUBSCRIPTION_FIELD_SPLITTER + email_token

def _get_subscription_code_and_email_token_from_extra_subscription_field(data):
    return data.split(EXTRA_SUBSCRIPTION_FIELD_SPLITTER)

class PaystackProvider(Gateway):

    def get_provider_type(self):
        return SubscriptionPaymantProvider.PAYSTACK

    def _create_plan(self, api, amount):
        res = api.post("plan", json={
            "name": "Doctor subscription", 
            "interval": "monthly", 
            "amount": amount,
        })
        plan_code = res.json()['data']['plan_code']
        return plan_code

    def _initialize_subscription(self, api, amount, plan_code):
        res = api.post("transaction/initialize", json={
            "email": "customer@email.com",
            "amount": amount,
            "plan": plan_code
        })
        data = res.json()['data']
        return plan_code, data['authorization_url']

    def _init_subscription(self, user: User, amount: int):
        api = PaystackAPI()
        plan_code = self._create_plan(api, amount)
        return self._initialize_subscription(api, amount, plan_code)

    def _subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        return self._init_subscription(user, amount)

    def _cancel_subscription(self, subscription: SubscriptionHistory):
        api = PaystackAPI()
        code, token = _get_subscription_code_and_email_token_from_extra_subscription_field(subscription.extra_gateway_values)
        res = api.post("subscription/disable", json={
            'code': code,
            'token': token,
        })
        return True

    def _verify_webhook(self, request):
        calculated_signature = hmac.new(settings.PAYSTACK_SECRET_KEY.encode('utf-8'), request.body, hashlib.sha512).hexdigest()
        signature = request.headers.get('X-Paystack-Signature')
        if calculated_signature != signature:
            raise PermissionDenied()

    def _is_webhook_update_data_type(self, data):
        return data['event'] == 'subscription.create'

    def _handle_update_data_webhook(self, data):
        data = data['data']
        subscription_code = data['subscription_code']
        email_token = data['email_token']
        plan_code = data['plan_code']
        subscription = SubscriptionHistory.objects.get(payment_ref=plan_code)
        extra_gateway_data = _get_extra_subscription_field(subscription_code, email_token)
        return subscription.id, plan_code, extra_gateway_data

    def _is_webhook_extension_type(self, data):
        return data['event'] == "charge.success"
        

    def _handle_extension_webhook(self, data):
        # TODO: Check how charge.success webhooks look1s like
        data = data['data']
        payment_ref = data['data']['plan']['plan_code']
        # TODO: Load subscription(get subscription id from history model) to get better values
        # start_time = datetime.strptime(data['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # end_time = datetime.strptime(data['data']['next_payment_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        start_time = datetime.strptime(data['paid_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = start_time + timedelta(days=30)
        new_payment_id = data['reference']
        return None, payment_ref, new_payment_id, start_time, end_time
