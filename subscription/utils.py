import json
from paypalrestsdk import BillingPlan
import requests
from requests.models import HTTPBasicAuth
from subscription.mixins import UserType
from user.models import ClinicInfo, DoctorInfo, PharmacyInfo, User


PAYPAL_API_BASE_URL = 'https://api-m.sandbox.paypal.com/v1/' # TODO: Move it to settings
PAYPAL_CLIENT_ID = 'AfM2LwelUElLMq3IzR0rhPt9acRf5WJBrHYAiKpnQcq4sKBVafVCFN19Ec0jGn5DW43ArWwpIyh-5l3E' # TODO: Move it to settings
PAYPAL_CLIENT_SECRET = 'EGom80tuePMavzuvJwcRlpUNqL_F17P1ryHAsFJ7lLmvki4TTO2Q89UTlqSlpFI92nyyQzIlloBDK3Ur'

class PayPalAPI():
    def __init__(self):
        self.paypal_token = None

    def authenticate(self):
        response = requests.post(PAYPAL_API_BASE_URL + 'oauth2/token', data={
            'grant_type': 'client_credentials'
        }, auth=HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET))
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        access_token = response_dict['access_token']
        expires_in = response_dict['expires_in']
        return access_token, expires_in

    def send(self, path, method, params={}, json={}):
        self.paypal_token = 'A21AAI4DjJ2nvv6UlrfhGhiTiSAEHAZEWT32tiwioJBJIdIUSbvdpMrWoVpOGBHB_hOj3mBe_IM9v53Q24z0WhLs500Rf3TZw'
        if not self.paypal_token:
            token, _ = self.authenticate() # TODO: Save token in cache
            self.paypal_token = token
        headers = {'Authorization': f'Bearer {self.paypal_token}'}
        print(headers)
        response = requests.request(method, PAYPAL_API_BASE_URL + path, params=params, json=json, headers=headers)
        if response.status_code not in [200, 201]:
            print(response.content)
            raise Exception()
        return response
    
    def create_billing_plan(self, data):
        return self.send('billing/plans', 'POST', {}, data)

    def create_billing_product(self, data):
        return self.send('catalogs/products', 'POST', {}, data)

def get_subscription_user(user: User):
    if user.user_type == UserType.CLINIC:
        return ClinicInfo.objects.get(user=user)
    if user.user_type == UserType.DOCTOR:
        return DoctorInfo.objects.get(user=user)
    if user.user_type == UserType.PHARMACY:
        return PharmacyInfo.objects.get(user=user)
    raise Exception()

def create_paypal_plan(name, price):
    product = PayPalAPI().create_billing_product({
        "name": "Video Streaming Service",
        "description": "Video streaming service",
        "type": "SERVICE",
        "category": "SOFTWARE",
    })
    print(product.json())
    product_id = product.json()['id']

    billing_plan = PayPalAPI().create_billing_plan({
        "product_id": product_id,
        "name": "Video Streaming Service Plan",
        "description": "Video Streaming Service basic plan",
        "status": "ACTIVE",
        "billing_cycles": [
            {
            "frequency": {
                "interval_unit": "MONTH",
                "interval_count": 1
            },
            "tenure_type": "TRIAL",
            "sequence": 1,
            "total_cycles": 2,
            "pricing_scheme": {
                "fixed_price": {
                "value": "3",
                "currency_code": "USD"
                }
            }
            },
            {
            "frequency": {
                "interval_unit": "MONTH",
                "interval_count": 1
            },
            "tenure_type": "TRIAL",
            "sequence": 2,
            "total_cycles": 3,
            "pricing_scheme": {
                "fixed_price": {
                "value": "6",
                "currency_code": "USD"
                }
            }
            },
            {
            "frequency": {
                "interval_unit": "MONTH",
                "interval_count": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 3,
            "total_cycles": 12,
            "pricing_scheme": {
                "fixed_price": {
                "value": "10",
                "currency_code": "USD"
                }
            }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
            "value": "10",
            "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        },
        "taxes": {
            "percentage": "10",
            "inclusive": False
        }
    })
    
    print("Billing Plan [%s] created successfully" % (billing_plan.json()['id']))
