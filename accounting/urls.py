from django.urls import path

from . import views

urlpatterns = [
    path("stripe-charge/", views.StripeChargeAPIView.as_view(), name="stripe_charge"),
    path("stripe-checkout/", views.StripeCheckoutAPIView.as_view(), name="stripe_checkout"),
    path(
        "paypal-verify/",
        views.PaypalProcessAPIView.as_view(),
        name="paypal_verify",
    ),
    path(
        "paypal-checkout/",
        views.PaypalCheckoutAPIView.as_view(),
        name="paypal_checkout",
    ),
    path(
        "paystack-verify/",
        views.PaystackVerifyAPIView.as_view(),
        name="paystack_verify",
    ),
    path(
        "flutterwave-charge/",
        views.FlutterwaveChargeAPIView.as_view(),
        name="flutterwave_charge",
    ),
    path(
        "flutterwave-checkout/",
        views.FlutterwaveCheckoutAPIView.as_view(),
        name="flutterwave_checkout",
    ),
]
