from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from paypalrestsdk import notifications
from django.conf import settings
from datetime import datetime
import stripe
import json

import requests
from .serializers import FlutterwaveChargeSerializer, FlutterwaveCheckoutSerializer, PaystackChargeSerializer, PaystackVerifySerializer, StripeChargeSerializer, StripeCheckoutSerializer, PaypalProcessSerializer, PaypalCheckoutSerializer
from .models import Payment
from appointment.models import Appointment



from .serializers import StripeChargeSerializer


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
    permission_classes = (AllowAny,)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        appointment_id = serializer.data["appointment_id"]
        print(appointment_id)
        appointment = Appointment.objects.get(pk=appointment_id)
        payment=Payment.objects.create( amount_paid =appointment.specialty.price, appointment= appointment, payment_gateway="Stripe",  )
        stripe_checkout_response = stripe.checkout.Session.create(
        success_url=f"https://example.com/success/{payment.id}",
        cancel_url=f"https://example.com/cancel/{payment.id}",#
        line_items=[
            {
            "price_data": {
                "currency":"usd",
                "product_data":{
                        "name":"Doctor Specialty: " + appointment.specialty.specialty ,
                        "description":"Description : " + appointment.description
                                },
                "unit_amount": payment.amount_paid
                            },
            "quantity": 1,
            },
                    ],
        mode="payment",
        client_reference_id=appointment_id,
        customer_email=appointment.patient.user.email,
    
        )
        payment.transaction_reference = stripe_checkout_response.id
        payment.payment_date = datetime.now()
        payment.save()
        url = stripe_checkout_response.url #return to frontend
        success_url = stripe_checkout_response.success_url
        cancel_url = stripe_checkout_response.cancel_url
        

        return Response(
            data={"checkout_url": url } )


class StripeCheckoutAPIView(generics.CreateAPIView):
    serializer_class = StripeCheckoutSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_id = serializer.data["payment_id"]
        try:
            payment = Payment.objects.get(id=payment_id)
            stripe_checkout_response = stripe.checkout.Session.retrieve(payment.transaction_reference)
            if stripe_checkout_response.payment_status == 'paid':
                payment.paid = True
                payment.appointment.payment = True
                payment.save()
        except:
            return Response("Invalid ID")

        return Response('success')
        



class PaypalProcessAPIView(generics.CreateAPIView):
    """
    Paypal payment verification webhook
    """

    permission_classes = (AllowAny,)
    serializer_class = PaypalProcessSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment_id = serializer.data["appointment_id"]
        appointment = Appointment.objects.get(pk=appointment_id)
        payment=Payment.objects.create( amount_paid =appointment.specialty.price, appointment= appointment, payment_gateway="Paypal",  )
        #auth=('user', 'pass')
        get_auth = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', data={"grant_type":"client_credentials"}, auth=("ARbTuLo_10qKxP2bF2fxgOWjifq13176ze0RsaVLHVEsg7Izg5ShIDaizj7B-qw6kyJ_hbDQ65P-ag-M","EBEb6D2MUxhl9AoN85M_FYYG8-jyNw3XDFo0sWl8rzsNXdcU2PKlAVQeyFn3X4zKlKeOp-0CEr53ael1") )
        token = get_auth.json()['access_token']

        create_charge = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', 
                        headers = {"Authorization": f"Bearer {token}"} ,
                        json = {
                        "intent": "CAPTURE",
                        "payer": appointment.patient.user.username,
                        "purchase_units": [
                            {
                            "amount": {
                                "currency_code": "USD",
                                "value": payment.amount_paid,
                                "description": appointment.description,
                                "payee": appointment.doctor.user.username
                            }
                            }
                        ],
                        "return_url": f"https://example.com/success/{payment.id}",
                        "cancel_url": f"https://example.com/cancel/{payment.id}",

                        })
        create_charge_json = create_charge.json()
        payment.transaction_reference = create_charge_json['id']
        payment.payment_date = datetime.now()
        payment.save()
        order_url = create_charge_json['links'][1]['href']
        
        return Response( data={"checkout_url" : order_url})

class PaypalCheckoutAPIView(generics.CreateAPIView):
    serializer_class = PaypalCheckoutSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_id = serializer.data["payment_id"]
        try:
            payment = Payment.objects.get(id=payment_id)
            print(Payment.objects.last())
            stripe_checkout_response = stripe.checkout.Session.retrieve(payment.transaction_reference)
            if stripe_checkout_response.payment_status == 'paid':
                payment.paid = True
                payment.appointment.payment = True
                payment.save()
        except:
            return Response("Invalid ID")

        return Response('success')

        


class FlutterwaveChargeAPIView(generics.CreateAPIView):
    """
    Flutterwave initialize payment
    """
    serializer_class = FlutterwaveChargeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment_id = serializer.data["appointment_id"]
        appointment = Appointment.objects.get(pk=appointment_id)
        payment=Payment.objects.create( amount_paid =appointment.specialty.price, appointment= appointment, payment_gateway="Flutterwave", )
        flutterwave_charge_url = f"https://api.flutterwave.com/v3/payments"
        flutterwave_charge_response = requests.post(flutterwave_charge_url,
        headers={"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}", "content_type": "application/json"}, 
        json = 
            {
            "tx_ref" : payment.id,
            "amount" : payment.amount_paid,
            "currency": "USD",
            "payment_options": "card",
            "redirect_url": f"https://example.com/success/",
            "customer": 
                {
                "name": appointment.patient.user.username,
                "email": appointment.patient.user.email,
                "phonenumber": appointment.patient.user.contact_no
                },
            "customizations":
                {
                "title":appointment.specialty.specialty,
                "description":appointment.description,
                "logo":"https://assets.piedpiper.com/logo.png"
                }
            }
        )


        return Response( data={ "checkout_url": flutterwave_charge_response.json()['data']['link']} )


class FlutterwaveCheckoutAPIView(generics.CreateAPIView):
    serializer_class = FlutterwaveCheckoutSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_id = serializer.data["tx_ref"]
        transaction_id = serializer.data["transaction_id"]
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.transaction_reference=transaction_id
            payment.save()
            flutterwave_verification_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
            flutterwave_verification_response = requests.post(flutterwave_verification_url, headers={"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}", "content_type": "application/json"}, )
            fvr_json = flutterwave_verification_response.json()
            if fvr_json['status']== 'success' and fvr_json['data']['currency'] == 'USD' and fvr_json['data']['amount'] ==payment.amount_paid :
                payment.paid = True
                payment.appointment.payment = True
                payment.payment_date = datetime.now()
                payment.save()
        except:
            return Response("Invalid transaction ID")

        return Response('success')


class PaystackChargeAPIView(generics.CreateAPIView):
    """
        Response example
        {'status': True,
        'message': 'Authorization URL created',
        'data': {'authorization_url': 'https://checkout.paystack.com/psw2iuzh6n55',
        'access_code': 'psw2iuzh6n55',
        'reference': '123456'}}
    """

    serializer_class = PaystackChargeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment_id = serializer.data["appointment_id"]
        appointment = Appointment.objects.get(pk=appointment_id)
        payment=Payment.objects.create( amount_paid =appointment.specialty.price, appointment= appointment, payment_gateway="Paystack", )
        paystack_charge_url = f"https://api.paystack.co/transaction/initialize"
        paystack_charge_response = requests.post(paystack_charge_url,
        headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}", "content_type": "application/json"}, 
        json =
        {
            "email": appointment.patient.user.email, 
            "amount": payment.amount_paid, 
            "currency": "USD",
            "reference":payment.id,
            "callback_url":"https://example.com/success/",
            "channels":["card",]
        })
        pcr_json = paystack_charge_response.json()

        payment.transaction_reference = pcr_json['data']['reference']
        payment.payment_date = datetime.now()
        payment.save()

        return Response( data={ "checkout_url": pcr_json['data']['authorization_url']} )



    

    
class PaystackVerifyAPIView(APIView):
    """
    Paystack payment verification
    Request body parameters:
    - transaction_reference

    return:
    - 200: if verification is successful
    - 400: if verification is unsuccessful
    """
    serializer_class = PaystackVerifySerializer
    permission_classes = (AllowAny,)

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reference = serializer.data["reference"]
        try:
            payment = Payment.objects.get(transaction_reference=reference)
            paystack_verify_url =  "https://api.paystack.co/transaction/verify/{reference}"
            paystack_verify_response = requests.get(paystack_verify_url, headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}", "content_type": "application/json"} )
            pvr_json = paystack_verify_response.json()
            if pvr_json['data']['status']== "success":
                payment.paid = True
                payment.appointment.payment = True
                payment.payment_date = datetime.now()
                payment.save()
        except:
            return Response("Invalid reference number")

        return Response('success')
       