from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

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


class CustomListUpdateAPIView(GenericAPIView):
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        payload = request.data
        for data in payload:
            instance_id = data.get("id")
            try:
                instance = get_object_or_404(self.get_queryset(), id=instance_id)
            except:
                instance = None
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)


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
