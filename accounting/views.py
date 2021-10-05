from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from paypalrestsdk import notifications
from django.conf import settings
import stripe
import json
import hashlib, hmac


from .serializers import StripeChargeSerializer
from Dokto_Backend.settings import SECRET_KEY


# TODO: Add Flutterwave webhook handler
# https://developer.flutterwave.com/v2.0/docs/events-webhooks
class FlutterwaveProcessWebhookAPIView(APIView):
    """
    Paystack payment verification webhook
    """

    @csrf_exempt
    def post(self, request):
        """
        Process webhook
        """
        # Get the payload
        payload = request.data
        return Response(status=status.HTTP_200_OK)


# TODO: Add Paystack webhook handler
# https://paystack.com/docs/payments/webhooks/
