from django.urls import path
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from .views import (FlutterwaveWebhook, PaypalWebhook, PaystackWebhook, StripeWebhook, SubscriptionView, UnsubscribeView, ChangeSubscriptionView)

urlpatterns = [
    path("subscribe/", SubscriptionView.as_view({'get': 'create'}), name="subscribe"),
    path("unsubscribe/", UnsubscribeView.as_view({'get': 'create'}), name="unsubscribe"),
    path("change_subscription_type/", ChangeSubscriptionView.as_view({'get': 'create'}), name="change-subscription-type"),
    path("flutterwave-webhook", authentication_classes([])(permission_classes([AllowAny])(FlutterwaveWebhook)).as_view()),
    path("paystack-webhook", PaystackWebhook.as_view(), name='paystack-webhook'),
    path("stripe-webhook", StripeWebhook.as_view()),
    path("paypal-webhook", PaypalWebhook.as_view(), name='paypal-webhook'),
]
