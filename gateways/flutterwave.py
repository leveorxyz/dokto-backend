from datetime import datetime, timedelta
import requests
import uuid
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.conf import settings
from stripe.api_resources import subscription
from gateways.gateway import Gateway
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider
from user.models import User


FLUTTERWAVE_BASE_URL = 'https://api.flutterwave.com/v3/'


class FlutterwaveAPI():
    def request(self, method, path, payload):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, FLUTTERWAVE_BASE_URL + path, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        if response_dict['status'] != 'success':
            raise Exception()
        return response_dict


class FluterwaveProviver(Gateway):

    def get_provider_type(self):
        return SubscriptionPaymantProvider.FLUTTERWAVE

    def _create_plan(self, api, total_amount):
        payload = {
            "amount": total_amount,
            "name": "Dokita Plan",
            "interval": "Monthly",
            "currency": "USD",
        }
        api = FlutterwaveAPI()
        response = api.request("POST", 'payment-plans', payload)
        plan_id = response['data']['id']
        return plan_id

    def _create_subscription(self, api, user, plan_id, total_amount):
        tx_ref = str(uuid.uuid4())
        payment_payload = {
            "tx_ref": tx_ref,
            "amount": total_amount / 100,
            "currency": "USD",
            "redirect_url":"https://webhook.site/9d0b00ba-9a69-44fa-a43d-a82c33c36fdc",
            "payment_options": "card",
            "payment_plan": plan_id,
            "meta":{
                "user_id": str(user.id),
            },
            "customer":{
                "email": user.email,
                "name": user.full_name
            },
            "customizations":{
                "title":"Dokita Subscription Payment",
                # "description":"Middleout isn't free. Pay the price",
                # "logo":"https://assets.piedpiper.com/logo.png"
            }
        }

        response_dict = api.request("POST", 'payments', payment_payload)
        payment_link = response_dict['data']['link']
        return tx_ref, payment_link

    def init_subscription(self, user: User, total_amount: int):
        api = FluterwaveProviver()
        plan_id = self._create_plan(api, total_amount)
        return self._create_subscription(api, user, plan_id, total_amount)

    def _subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        return self.init_subscription(user, amount)

    def _cancel_subscription(self, subscription: SubscriptionHistory):
        path = f'subscriptions/{subscription.extra_gateway_values}/cancel'
        FlutterwaveAPI().request("POST", path, {})
        return True

    def _verify_webhook(self, request):
        if request.headers.get('Verif-Hash') != settings.FLUTTERWAVE_WEBHOOK_VERIFICATION_HASH:
            raise AuthenticationFailed()

    def _get_subscription_id_for_subscription_history(self, subscription: SubscriptionHistory):
        api = FlutterwaveAPI()
        res = api.request('GET', 'subscriptions', {}, {'plan': subscription.payment_ref})
        flutter_subscriptions = res['data']
        flutter_subscription = None
        for sub in flutter_subscriptions:
            if sub['customer']['customer_email'] == subscription.user.email:
                flutter_subscription = sub
        return flutter_subscription['id']
        

    def _handle_webhook(self, data):
        if not data.get('paymentPlan'):
            return
        transaction_id = data.get('id')
        payment_url = FLUTTERWAVE_BASE_URL + f'transactions/{transaction_id}/verify'
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.request("GET", payment_url, headers=headers)
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        if response_dict['status'] != 'success':
            raise Exception()
        data = response_dict['data']
        user_id = data['meta']['user_id']
        payment_ref = data['paymentPlan']
        
        subscription: SubscriptionHistory = SubscriptionHistory.objects.filter(payment_method=self.get_payment_gateway())(payment_ref=payment_ref).first()
        if not subscription.extra_gateway_values:
            sub_id = self._get_subscription_id_for_subscription_history(subscription)
            subscription.extra_gateway_values = sub_id
            subscription.save()
        # TODO: Explore other ways to get these values
        start_time_string = data['created_at']
        start_time = datetime.strptime(start_time_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = start_time + timedelta(days=30)
        
        return payment_ref, start_time_string, start_time, end_time