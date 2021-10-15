from django.urls import path

from .views import UserRetrieveAPIView, LoginView

urlpatterns = [
    path("<int:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
]
