from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from paypalrestsdk import notifications
from django.conf import settings
import stripe
import json
import requests
import hashlib, hmac


from .serializers import StripeChargeSerializer


class FlutterwaveVerifyAPIView(APIView):
    """
    Flutterwave payment verification
    Request body parameters:
    - transaction_reference
    - appointment_id
    return:
    - 200: if verification is successful
    - 400: if verification is unsuccessful
    """

    def post(self, request):
        # Extracting reference and appointment_id from request
        request_body = json.loads(request.body)

        # If reference is not present in request body throw error
        if not "transaction_reference" in request_body:
            raise ValidationError(detail="No reference string in body")

        # Sending request to flutterwave to verify the transaction
        flutterwave_verification_url = f"https://api.flutterwave.com/v3/transactions/{request_body['transaction_reference']}/verify"
        flutterwave_verification_response = requests.get(
            flutterwave_verification_url,
            headers={
                "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                "content_type": "application/json",
            },
        )
        flutterwave_verification_response_json = (
            flutterwave_verification_response.json()
        )
        print(flutterwave_verification_response_json)

        # If transaction is not successful throw error else return success
        if flutterwave_verification_response_json["status"] == "success":
            #  Checkout successful, do something
            return Response(
                data={
                    "status_code": 200,
                    "message": flutterwave_verification_response_json["message"],
                    "result": {
                        "created_at": flutterwave_verification_response_json["data"][
                            "created_at"
                        ],
                    },
                },
                status=status.HTTP_200_OK,
            )

        # Verification failed
        return Response(
            data={
                "status_code": 400,
                "message": flutterwave_verification_response_json["message"],
                "result": None,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class PaystackVerifyAPIView(APIView):
    """
    Paystack payment verification
    Request body parameters:
    - transaction_reference
    - appointment_id

    return:
    - 200: if verification is successful
    - 400: if verification is unsuccessful
    """

    def post(self, request):
        # Extracting reference and appointment_id from request
        request_body = json.loads(request.body)

        # If reference is not present in request body throw error
        if not "transaction_reference" in request_body:
            raise ValidationError(detail="No reference string in body")

        # Sending request to paystack to verify the transaction
        paystack_verification_url = f"https://api.paystack.co/transaction/verify/{request_body['transaction_reference']}"
        paystack_verification_response = requests.get(
            paystack_verification_url,
            headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
        )
        paystack_verification_response_json = paystack_verification_response.json()

        # If transaction is not successful throw error else return success
        if paystack_verification_response_json["status"] == True:
            #  Checkout successful, do something
            return Response(
                data={
                    "status_code": 200,
                    "message": paystack_verification_response_json["message"],
                    "result": {
                        "paid_at": paystack_verification_response_json["data"][
                            "paid_at"
                        ],
                        "created_at": paystack_verification_response_json["data"][
                            "created_at"
                        ],
                    },
                },
                status=status.HTTP_200_OK,
            )

        # Verification failed
        return Response(
            data={
                "status_code": 400,
                "message": paystack_verification_response_json["message"],
                "result": None,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
