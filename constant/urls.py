from django.urls import path

from . import views

urlpatterns = [
    path("available-care/", view=views.AvailableCare.as_view(), name="available_care"),
]
