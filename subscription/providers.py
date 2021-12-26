from datetime import datetime
import base64
import requests
import uuid
from requests.models import HTTPBasicAuth
from rest_framework.exceptions import AuthenticationFailed
import stripe
from django.conf import settings
import subscription
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider, SubscriptionPlanTypes
from subscription.serializers import SubscriptionChargeSerializer
from subscription.utils import PayPalAPI

from user.models import User


stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PLAN_T0_PRICE_CONVERSION_DICT = {
    SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE: '',
    SubscriptionPlanTypes.PHARMACY_SUBSCRIPTION_PLAN: '',
    SubscriptionPlanTypes.CLINIC_SUBSCRIPTION_PLAN: '',
    SubscriptionPlanTypes.DOCTOR_WITH_HOME_SERVICE: '',
}


PAYPAL_SUBSCRIPTION_RETURN_URL = 'AAA' # TODO: Move it to settings
PAYPAL_SUBSCRIPTION_CANCEL_URL = 'AAA' # TODO: Move it to settings
PAYPAL_PLAN_T0_PLAN_ID_CONVERSION_DICT = {
    SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE: '',
    SubscriptionPlanTypes.PHARMACY_SUBSCRIPTION_PLAN: '',
    SubscriptionPlanTypes.CLINIC_SUBSCRIPTION_PLAN: '',
    SubscriptionPlanTypes.DOCTOR_WITH_HOME_SERVICE: '',
}


FLUTTERWAVE_BASE_URL = 'https://api.flutterwave.com/v3/' # TODO: Move it to settings
FLUTTERWAVE_WEBHOOK_VERIFICATION_HASH = 'sssssss'

class StripeProvider():
    def create_subscription(self, user: User, no_of_doctors: int, payment_method_id: str, stripe_price_id: str):
        customer = stripe.Customer.create(
            email = user.email,
            payment_method=payment_method_id
        )
        print(customer)
        subscription_data = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {'price': stripe_price_id, 'quantity': no_of_doctors},
            ],
        )
        print(subscription_data)
        return subscription_data.id, ""
    
    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int, serializer: SubscriptionChargeSerializer):
        return self.create_subscription(user, quantity, serializer.stripe_payment_method_id, STRIPE_PLAN_T0_PRICE_CONVERSION_DICT.get(plan_type))


class PaystackProvider():
    pass


class PaypalProvider():

    def init_subscription(self, user: User, no_of_doctors: int, paypal_plan_id: str):
        response = PayPalAPI().send("POST", 'billing/subscriptions', json={
            'plan_id': paypal_plan_id,
            'start_time': datetime.now(),
            'quantity': no_of_doctors, # TODO: ISSUE Max is 32
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
                        'address_line_1': '2211 N First Street',
                        'address_line_2': 'Building 17',
                        'admin_area_2': 'San Jose',
                        'admin_area_1': 'CA',
                        'postal_code': '95131',
                        'country_code': 'US'
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

    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        return self.init_subscription(user, quantity, PAYPAL_PLAN_T0_PLAN_ID_CONVERSION_DICT.get(plan_type))
        

class FluterwaveProviver():
    def init_subscription(self, user: User, total_amount: int):
        import requests

        url = FLUTTERWAVE_BASE_URL + 'payment-plans'

        payload = {
            "amount": total_amount,
            "name": "Dokita Plan",
            "interval": "Monthly",
            "currency": "USD",
        }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        if response_dict['status'] != 'success':
            raise Exception()
        plan_id = response_dict['data']['id']
        
        tx_ref = str(uuid.uuid4())
        payment_payload = {
            "tx_ref": tx_ref,
            "amount": total_amount,
            "currency": "USD",
            "redirect_url":"https://webhook.site/9d0b00ba-9a69-44fa-a43d-a82c33c36fdc",
            "payment_options": "card",
            "payment_plan": plan_id,
            "meta":{
                "user_id": str(user.id),
                # "consumer_mac":"92a3-912ba-1192a"
            },
            "customer":{
                "email": user.email,
                # "phonenumber":"080****4528",
                "name": user.full_name
            },
            "customizations":{
                "title":"Dokita Subscription Payment",
                # "description":"Middleout isn't free. Pay the price",
                # "logo":"https://assets.piedpiper.com/logo.png"
            }
        }
        payment_url = FLUTTERWAVE_BASE_URL + 'payments'
        response = requests.request("POST", payment_url, json=payment_payload, headers=headers)
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        if response_dict['status'] != 'success':
            raise Exception()
        payment_link = response_dict['data']['link']
        return tx_ref, payment_link

    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        return self.init_subscription(user, amount)


    def handle_webhook(self, webhook):
        if webhook.headers.get('verif-hash') != FLUTTERWAVE_WEBHOOK_VERIFICATION_HASH:
            raise AuthenticationFailed()
        if not webhook.data.get('paymentPlan'):
            return
        # TODO: For extra layer of security, we might want to verify payment on flutterwave
        transaction_id = webhook.data.get('id')
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
        payment_ref = data['tx_ref']
        subscription = SubscriptionHistory.objects.filter(user__id=user_id).filter(payment_ref=payment_ref).first()
        # TODO: Verify that this is enough for subsequent months
        subscription.set_paid()
        



providers_dict = {
    SubscriptionPaymantProvider.FLUTTERWAVE: FluterwaveProviver(),
    SubscriptionPaymantProvider.PAYPAL: PaypalProvider(),
    SubscriptionPaymantProvider.PAYSTACK: PaystackProvider(),
    SubscriptionPaymantProvider.STRIPE: StripeProvider(),
}

class Provider():
    def __init__(self, subscriptionType: str):
        self.provider = providers_dict[subscriptionType]
        self.provider_type = subscriptionType
        
    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        id, approval_url = self.provider.subscribe(user, amount, plan_type, quantity)
        history = SubscriptionHistory()
        history.user = user
        history.payment_ref = id
        history.payment_method = self.provider_type
        history.save()
        return id, approval_url
