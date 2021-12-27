from datetime import datetime
from rest_framework.exceptions import PermissionDenied
import stripe
from django.conf import settings
from gateways.gateway import Gateway
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider, SubscriptionPlanTypes
from subscription.serializers import SubscriptionChargeSerializer

from user.models import User

STRIPE_SUBSCRIPTIOM_SUCCESS_URL = 'https://example.com/success' # TODO: Collect from frontend
STRIPE_SUBSCRIPTIOM_CANCEL_URL = 'https://example.com/cancel' # TODO: Collect from frontend
SUBSCRIPTION_HISTORY_ID_METADATA_KEY = 'subscription_history_id'

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SIGNATURE = settings.STRIPE_WEBHOOK_SIGNATURE
STRIPE_PLAN_T0_PRICE_CONVERSION_DICT = {
    SubscriptionPlanTypes.DOTOR_SUSBCRIPTION_TYPE: settings.STRIPE_DOTOR_SUSBCRIPTION_PRICE,
    SubscriptionPlanTypes.PHARMACY_SUBSCRIPTION_PLAN: settings.STRIPE_PHARMACY_SUBSCRIPTION_PRICE,
    SubscriptionPlanTypes.CLINIC_SUBSCRIPTION_PLAN: settings.STRIPE_CLINIC_SUBSCRIPTION_PRICE,
    SubscriptionPlanTypes.DOCTOR_WITH_HOME_SERVICE: settings.STRIPE_DOCTOR_WITH_HOME_SERVICE_PRICE,
}


class SupportedStripeEventTypes:
    SUBSCRIPTION_CREATED = 'customer.subscription.created'
    all = [SUBSCRIPTION_CREATED, ]
    subscription_extended_statuses = [SUBSCRIPTION_CREATED]


class StripeProvider(Gateway):
    def create_subscription(self, user: User, no_of_doctors: int, source_id: str, stripe_price_id: str, history: SubscriptionHistory):
        customer = stripe.Customer.create(
            email = user.email,
            source=source_id
        )
        subscription_data = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {'price': stripe_price_id, 'quantity': no_of_doctors},
            ],
        )
        session = stripe.checkout.Session.create(
            success_url=STRIPE_SUBSCRIPTIOM_SUCCESS_URL,
            cancel_url=STRIPE_SUBSCRIPTIOM_CANCEL_URL,
            line_items=[
                {
                    "price": stripe_price_id,
                    "quantity": no_of_doctors,
                },
            ],
            mode="subscription",
            metadata={
                SUBSCRIPTION_HISTORY_ID_METADATA_KEY: history.id
            }
        )
        return None, ""

    def _subscribe(self, user: User, amount: int, plan_type: str, quantity: int, serializer: SubscriptionChargeSerializer, history: SubscriptionHistory=None):
        return self.create_subscription(user, quantity, serializer.stripe_payment_method_id, STRIPE_PLAN_T0_PRICE_CONVERSION_DICT.get(plan_type), history)

    def _is_webhook_update_data_type(self, data):
        event_type = data.get('type')
        if event_type == 'checkout.session.completed' and data['data']['mode'] == 'subscription':
            return True
        return False

    def _is_webhook_extension_type(self, data):
        event_type = data.get('type')
        if event_type in [
            "customer.subscription.created",
            "customer.subscription.updated",   
        ]:
            return True
        return False

    def _handle_update_data_webhook(self, data):
        history_id = data['data']['metadata'][SUBSCRIPTION_HISTORY_ID_METADATA_KEY]
        subscription_id = data['data']['subscription']
        return history_id, subscription_id

    def _verify_webhook(self, request):
        if(request.headers.get('stripe-signature')) != STRIPE_WEBHOOK_SIGNATURE:
            raise PermissionDenied()

    def _handle_extension_webhook(self, data):
        subscription_id = data['object']['id']
        status = data['status']
        if status != 'active':
            return ;
        start_time = datetime.fromtimestamp(data['current_period_start'])
        end_time = datetime.fromtimestamp(data['current_period_end'])
        invoice_id = data['latest_invoice']
        return subscription_id, invoice_id, start_time, end_time
