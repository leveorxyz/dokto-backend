from datetime import datetime, time, timedelta
import base64
import hashlib
import hmac
from django.http import response
import requests
import uuid
from requests.models import HTTPBasicAuth
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
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

class SupportedStripeEventTypes:
    SUBSCRIPTION_CREATED = 'customer.subscription.created'
    all = [SUBSCRIPTION_CREATED, ]
    subscription_extended_statuses = [SUBSCRIPTION_CREATED]



PAYPAL_SUBSCRIPTION_RETURN_URL = 'https://example.com/' # TODO: Move it to settings
PAYPAL_SUBSCRIPTION_CANCEL_URL = 'https://example.com/' # TODO: Move it to settings
PAYPAL_PLAN_T0_PLAN_ID_CONVERSION_DICT = {
    SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE: '',
    SubscriptionPlanTypes.PHARMACY_SUBSCRIPTION_PLAN: '',
    SubscriptionPlanTypes.CLINIC_SUBSCRIPTION_PLAN: '',
    SubscriptionPlanTypes.DOCTOR_WITH_HOME_SERVICE: '',
}
STRIPE_WEBHOOK_SIGNATURE = 'aaaa'

PAYSTACK_SECRET_KEY = 'sk_test_b8fdadbb4426e37276abdf0a28528b4085ddb4a9'

FLUTTERWAVE_BASE_URL = 'https://api.flutterwave.com/v3/' # TODO: Move it to settings
FLUTTERWAVE_WEBHOOK_VERIFICATION_HASH = 'sssssss'

class StripeProvider():
    def create_subscription(self, user: User, no_of_doctors: int, source_id: str, stripe_price_id: str):
        customer = stripe.Customer.create(
            email = user.email,
            source=source_id
        )
        # print(customer)
        subscription_data = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {'price': stripe_price_id, 'quantity': no_of_doctors},
            ],
        )
        return subscription_data.id, ""

    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int, serializer: SubscriptionChargeSerializer):
        return self.create_subscription(user, quantity, serializer.stripe_payment_method_id, STRIPE_PLAN_T0_PRICE_CONVERSION_DICT.get(plan_type))

    def handle_webhook(self, request):
        if(request.headers.get('stripe-signature')) != STRIPE_WEBHOOK_SIGNATURE:
            raise PermissionDenied()
        data = request.data
        event_type = data.get('type')
        if event_type not in SupportedStripeEventTypes.all:
            return ;
        if event_type in SupportedStripeEventTypes.subscription_extended_statuses:
            subscription_id = data['object']['id']
            subscription = SubscriptionHistory.objects.filter(payment_ref=subscription_id).filter(payment_method=SubscriptionPaymantProvider.STRIPE).first()
            if not subscription:
                raise Exception()
            status = data['status']
            if status != 'active':
                return ;
            start_time = datetime.fromtimestamp(data['current_period_start'])
            end_time = datetime.fromtimestamp(data['current_period_end'])
            invoice_id = data['latest_invoice']
            subscription.add_new_payment(invoice_id, start_time, end_time)


class PaystackEventType:
    SUBSCRIPTION_CREATED = 'subscription.create'
    all = [SUBSCRIPTION_CREATED]

class PaystackProvider():
    def init_subscription(self, user: User, amount: int):
        res = requests.post("https://api.paystack.co/plan", json={ "name": "Monthly Retainer", 
            "interval": "monthly", 
            "amount": amount,
        }, headers={
            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'
        })
        if res.status_code != 201:
            raise Exception()
        plan_code = res.json()['data']['plan_code']
        res = requests.post("https://api.paystack.co/transaction/initialize", json={
            "email": "customer@email.com",
            "amount": amount,
            "plan": plan_code
        }, headers={
            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'
        })
        if res.status_code != 200:
            raise Exception()
        data = res.json()['data']
        return plan_code, data['authorization_url']
        

    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        return self.init_subscription(user, amount)

    def handle_webhook(self, request):
        calculated_signature = hmac.new(PAYSTACK_SECRET_KEY.encode('utf-8'), request.body, hashlib.sha512).hexdigest()
        signature = request.headers.get('X-Paystack-Signature')
        if calculated_signature != signature:
            raise PermissionDenied()
        data = request.data
        event_type = data['event']
        if event_type not in PaystackEventType.all:
            print(8888)
            return ;
        if data['data']['status'] != 'active':
            return ;
        payment_ref = data['data']['plan']['plan_code']
        subscription = SubscriptionHistory.objects.filter(payment_ref=payment_ref).filter(payment_method=SubscriptionPaymantProvider.PAYSTACK).first()
        start_time = datetime.strptime(data['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = datetime.strptime(data['data']['next_payment_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        id = data['data']['id']
        print(start_time)
        subscription.add_new_payment(id, start_time, end_time)
        
        
class PaypalEventTypes:
    SUBSCRIPTION_CREATED = 'BILLING.SUBSCRIPTION.ACTIVATED'
    all = [SUBSCRIPTION_CREATED,]

class PaypalProvider():

    def init_subscription(self, user: User, no_of_doctors: int, paypal_plan_id: str):
        response = PayPalAPI().send('billing/subscriptions', "POST", json={
            'plan_id': paypal_plan_id,
            'start_time': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
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

    def verify_webhook(self, request):
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
        start_time_string = obj['billing_info']['last_payment']['time'] # Np payment ID from paypal but payment time can 
                                                                        # also uniquely identify a subscription payment
        start_time = datetime.strptime(start_time_string, '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.strptime(obj['billing_info']['next_billing_time'], '%Y-%m-%dT%H:%M:%SZ')
        subscription = SubscriptionHistory.objects.filter(payment_ref=subscription_id).filter(payment_method=SubscriptionPaymantProvider.PAYPAL).first()
        subscription.add_new_payment(start_time_string, start_time, end_time)

    def handle_webhook(self, request):
        if not self.verify_webhook(request):
            raise Exception()
        self._handle_webhook(request.data)

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
