from enum import Enum

from stripe.api_resources import subscription
from subscription.models import SubscriptionHistory, SubscriptionPaymantProvider
from user.models import User

class WebhookTypes(Enum):
    subscription_extension = "S"
    subscription_data_update = "U"
    subscription_cancellation = "C"
    others = "O"

class Gateway():

    def get_provider_type(self):
        raise NotImplemented

    def _subscribe(self, user: User, amount: int, plan_type: str, quantity: int, history: SubscriptionHistory=None):
        raise NotImplemented

    def subscribe(self, user: User, amount: int, plan_type: str, quantity: int):
        history = SubscriptionHistory()
        history.user = user
        history.payment_method = self.get_provider_type()
        history.amount = amount
        history.save()
        id, approval_url = self._subscribe(user, amount, plan_type, quantity, history=history)
        history.payment_ref = id
        history.save()
        return id, approval_url

    def _verify_webhook(self, request):
        raise NotImplemented

    def _is_webhook_update_data_type(self, data):
        pass

    def _is_webhook_extension_type(self, data):
        pass

    def _is_webhook_cancellation_type(self, data):
        pass

    def _handle_update_data_webhook(self, data):
        pass

    def _handle_extension_webhook(self, data):
        pass

    def _handle_webhook(self, data):
        if self._is_webhook_update_data_type(data):
            result = self._handle_update_data_webhook(data)
            if result:
                history_id, subscription_id = result
                history = SubscriptionHistory.objects.get(pk=history_id)
                history.payment_ref = subscription_id
                history.save()
        if self._is_webhook_extension_type(data):
            result = self._handle_extension_webhook(data)
            if result:
                payment_ref, new_payment_id, start_time, end_time = result
                subscription = SubscriptionHistory.objects.filter(payment_ref=payment_ref).filter(payment_method=self.get_provider_type()).first()
                subscription.add_new_payment(id, start_time, end_time)
        if self._is_webhook_cancellation_type(data):
            return;

    def handle_webhook(self, request):
        self._verify_webhook(request)
        result = self._handle_webhook(request.data)
        if not result:
            return
        payment_ref, new_payment_id, start_time, end_time = result
        subscription = SubscriptionHistory.objects.filter(payment_ref=payment_ref).filter(payment_method=self.get_provider_type()).first()
        subscription.add_new_payment(id, start_time, end_time)
        

    @staticmethod
    def get_payment_gateway(provider):
        from .flutterwave import FluterwaveProviver
        from .paypal import PaypalProvider
        from .paystack import PaystackProvider
        from .stripe import StripeProvider

        providers_dict = {
            SubscriptionPaymantProvider.FLUTTERWAVE: FluterwaveProviver(),
            SubscriptionPaymantProvider.PAYPAL: PaypalProvider(),
            SubscriptionPaymantProvider.PAYSTACK: PaystackProvider(),
            SubscriptionPaymantProvider.STRIPE: StripeProvider(),
        }
        provider = providers_dict[provider]
        return provider
