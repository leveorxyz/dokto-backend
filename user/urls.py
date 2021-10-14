from django.urls import path

from .views import UserRetrieveAPIView

urlpatterns = [
    path("<int:pk>", UserRetrieveAPIView.as_view(), name="user-retrieve"),
]
