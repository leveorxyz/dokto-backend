from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from paypalrestsdk import notifications
from django.conf import settings
import stripe
import json
import hashlib, hmac


from .serializers import (StripeChargeSerializer)
from Dokto_Backend.settings import SECRET_KEY


class StripeChargeAPIView(generics.CreateAPIView):
    """
    1. GET TOKEN_ID, DESCRIPTION, CURRENCY, AMOUNT FROM FRONTEND
    2. try:
    stripe.Charge.create(
        amount is in cents: i.e 999 is 9.99
        amount=request.POST.get('amount', ''),
        currency=request.POST.get('currency', ''),
        source=request.POST.get('source', ''),  # token.id
        description=request.POST.get('description', '')
        statement_descriptor will appear in user's credit card statement
        statement_descriptor="Company XYX",
        metadata={"order_id": 123456}
    )
    Statement descriptors are limited to 22 characters, cannot use the
        special characters <, > , ', or ", and must not consist solely of numbers.
        metadata is the opposite and will only appear in your DASHBOARD(e.g when
                                                                        looking at the page for an individual charge) and is also available in common
        reports and exports. As an example, your store's order ID can be attached to
        the charge used to pay for that order.
        (!!! DONT STORE ANY SENSITIVE INFORMATION - CARD DETAILS ETC as metadata or
         in the charge's description parameter)

    3. Return response to my frontend to display a confirmation / error
    """
    serializer_class = StripeChargeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        token = serializer.data.get('token')

        try:
            charge = stripe.Charge.create(
                amount=100,
                currency='usd',
                description="Description",
                source=token,
                receipt_email="receipt email",
                shipping={
                    "name": "customer name",
                    "phone": "",
                    'address': {
                        "country": "",
                        "line1": "",
                        "line2": "",
                        "postal_code": "",
                    }
                }
            )
            print(charge)

        except Exception as e:
            return Response(data={'status': 400, 'message': e.error.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'status': 200, 'message': 'success'}, status=status.HTTP_201_CREATED)


class PaypalProcessWebhookAPIView(APIView):
    """
    Paypal payment verification webhook
    """

    def post(self, request):
        if "HTTP_PAYPAL_TRANSMISSION_ID" not in request.META:
            return Response(data={'status': 400, 'message': 'Bad Request'})

        auth_algo = request.META['HTTP_PAYPAL_AUTH_ALGO']
        cert_url = request.META['HTTP_PAYPAL_CERT_URL']
        transmission_id = request.META['HTTP_PAYPAL_TRANSMISSION_ID']
        transmission_sig = request.META['HTTP_PAYPAL_TRANSMISSION_SIG']
        transmission_time = request.META['HTTP_PAYPAL_TRANSMISSION_TIME']
        webhook_id = settings.PAYPAL_WEBHOOK_ID
        event_body = request.body.decode(request.encoding or "utf-8")

        valid = notifications.WebhookEvent.verify(
            transmission_id=transmission_id,
            timestamp=transmission_time,
            webhook_id=webhook_id,
            event_body=event_body,
            cert_url=cert_url,
            actual_sig=transmission_sig,
            auth_algo=auth_algo,
        )

        if not valid:
            return Response(data={'status': 400, 'message': 'Invalid Transaction'}, status=status.HTTP_400_BAD_REQUEST)

        webhook_event = json.loads(event_body)

        event_type = webhook_event["event_type"]

        CHECKOUT_ORDER_APPROVED = "CHECKOUT.ORDER.APPROVED"

        if event_type == CHECKOUT_ORDER_APPROVED:
            #  Checkout successfull, do something
            pass
        return Response(data={'status': 200, 'message': 'Bad Request'}, status=status.HTTP_200_OK)

# TODO: Add Flutterwave webhook handler
# https://developer.flutterwave.com/v2.0/docs/events-webhooks

# TODO: Add Paystack webhook handler
# https://paystack.com/docs/payments/webhooks/
class PaystackProcessWebhookAPIView(APIView):
    """
    Paystack payment verification webhook
    """
    def post(self, request):
        hash = hmac.new(SECRET_KEY, digestmod=hashlib.sha512).update(request.body).hexdigest()
        print(hash)
        return Response(status=status.HTTP_200_OK)