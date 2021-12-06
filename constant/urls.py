from django.urls import path

from . import views

urlpatterns = [
    path("available-care/", view=views.AvailableCare.as_view(), name="available_care"),
    path("country/", view=views.Country.as_view(), name="country"),
    path("state/", view=views.State.as_view(), name="state"),
    path("city/", view=views.City.as_view(), name="city"),
    path("phone-code/", view=views.PhoneCode.as_view(), name="phone_code"),
    path(
        "accepted-insurance/",
        view=views.AcceptedInsurance.as_view(),
        name="accepted_insurance",
    ),
    path("profession/", view=views.ProfessionView.as_view(), name="profession"),
    path(
        "profession-service/",
        view=views.ServicesView.as_view(),
        name="profession_service",
    ),
]
