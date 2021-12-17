from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.OnboardMailAPIView.as_view(), name="onboard_mail"),
]
