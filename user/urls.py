from django.urls import path

from .views import UserRetrieveAPIView, LoginView, UsernameExists

urlpatterns = [
    path("<int:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
    path("exists/<str:username>", UsernameExists.as_view(), name="username-exists"),
]
