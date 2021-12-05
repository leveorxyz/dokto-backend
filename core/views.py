from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from core.mixins import CustomListUpdateModelMixin, CustomListModelMixin
from .utils import set_user_ip

# Create your views here.


def custom_response(response):
    response_data = {
        "message": "success",
        "status_code": response.status_code,
        "result": response.data,
    }
    response.data = response_data
    return response


class CustomRetrieveAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomListUpdateAPIView(
    GenericAPIView, CustomListModelMixin, CustomListUpdateModelMixin
):
    pagination_class = None

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
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


class CustomAPIView(APIView):
    http_method_names = ["get", "post", "patch", "put", "delete", "head", "options"]

    def get(self, data=None, *args, **kwargs):
        if not data:
            data = {}
        response = Response(data)
        return custom_response(response)

    def post(self, data=None, *args, **kwargs):
        return self.get(data, *args, **kwargs)

    def patch(self, data=None, *args, **kwargs):
        return self.get(data, *args, **kwargs)

    def put(self, data=None, *args, **kwargs):
        return self.get(data, *args, **kwargs)

    def delete(self, data=None, *args, **kwargs):
        return self.get(data, *args, **kwargs)
