from django.urls import path

from . import views

urlpatterns = [
    path('stripe-charge/', views.StripeChargeAPIView.as_view(), name="stripe_charge")
]
