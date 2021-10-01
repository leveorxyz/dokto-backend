from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

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
        return custom_response(response)


class CustomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return custom_response(response)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return custom_response(response)


class CustomCreateAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return custom_response(response)


class CustomListAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return custom_response(response)


class CustomListCreateAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return custom_response(response)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return custom_response(response)


class CustomRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return custom_response(response)