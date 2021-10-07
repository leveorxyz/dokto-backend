from django.urls import path

from . import views

urlpatterns = [
    path(
        "flutterwave-verify/",
        views.FlutterwaveVerifyAPIView.as_view(),
        name="flutterwave_verify",
    ),
]
