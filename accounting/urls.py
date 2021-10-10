from django.urls import path

from . import views

urlpatterns = [
    path(
        "paypal-verify/",
        views.PaypalProcessWebhookAPIView.as_view(),
        name="paypal_verify",
    ),
    path(
        "paystack-verify/",
        views.PaystackVerifyAPIView.as_view(),
        name="paystack_verify",
    ),
        "flutterwave-verify/",
        views.FlutterwaveVerifyAPIView.as_view(),
        name="flutterwave_verify",
    ),
]
