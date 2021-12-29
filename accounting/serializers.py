from rest_framework import serializers


class StripeChargeSerializer(serializers.Serializer):
    """
    Stripe Charge Serializer
    """

    appointment_id = serializers.CharField()
    # token = serializers.CharField()

class StripeCheckoutSerializer(serializers.Serializer):
    """Stripe COnfirm payment status"""

    payment_id=serializers.CharField()

class PaypalProcessSerializer(serializers.Serializer):
    """Paypal Process chARGE"""

    appointment_id=serializers.CharField()


class PaypalCheckoutSerializer(serializers.Serializer):
    """Paypal Checkout/Confirm payment"""

    appointment_id=serializers.CharField()



class FlutterwaveChargeSerializer(serializers.Serializer):
    """Flutterwave Charge Payment"""

    appointment_id = serializers.CharField()


class FlutterwaveCheckoutSerializer(serializers.Serializer):
    """Flutterwave Confirm Payment wiith payment_id"""

    tx_ref = serializers.CharField()
    transaction_id = serializers.CharField()


class PaystackChargeSerializer(serializers.Serializer):
    """Paystak Charge Payment"""

    appointment_id = serializers.CharField()



class PaystackVerifySerializer(serializers.Serializer):
    """Paystack Verify Payment Serializer"""

    payment_id = serializers.CharField()
    reference = serializers.CharField()