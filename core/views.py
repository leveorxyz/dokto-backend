from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from user.models import UserIp

# Create your views here.


def custom_response(response):
    response_data = {
        "message": "success",
        "status_code": response.status_code,
        "result": response.data,
    }
    response.data = response_data
    return response


def set_user_ip(request):
    ip = None
    user = request.user
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    if user.is_authenticated:
        x = UserIp.objects.update_or_create(user=user, ip=ip)
        print(x)


class CustomRetrieveAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomCreateAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomListAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomListCreateAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)
