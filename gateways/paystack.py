from datetime import datetime, time, timedelta
import hashlib
import hmac
import requests
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
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


class PaystackProvider(Gateway):

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

    def _verify_webhook(self, request):
        calculated_signature = hmac.new(settings.PAYSTACK_SECRET_KEY.encode('utf-8'), request.body, hashlib.sha512).hexdigest()
        signature = request.headers.get('X-Paystack-Signature')
        if calculated_signature != signature:
            raise PermissionDenied()

    def _handle_webhook(self, data):
        # TODO: Check if the reference will always come with paystack charge webhook tomorrow
        # TODO: Consider metadata and customer email as well
        # TODO: Options => Add one more field to save subscription_id, then load subscription on each webhook
        event_type = data['event']
        if event_type not in PaystackEventType.all:
            return ;
        if data['data']['status'] != 'active':
            return ;
        payment_ref = data['data']['plan']['plan_code']
        start_time = datetime.strptime(data['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = datetime.strptime(data['data']['next_payment_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        new_payment_id = data['data']['id']
        return payment_ref, new_payment_id, start_time, end_time
