from django.urls import path

from . import views

urlpatterns = [
    path("stripe-charge/", views.StripeChargeAPIView.as_view(), name="stripe_charge"),
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
]
