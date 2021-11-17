from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from django.http import JsonResponse


class Custom404(APIView):
    def get(self, *args, **kwargs):
        response_data = {
            "message": ["Not found!"],
            "status_code": 404,
            "result": None,
        }
        return Response(response_data, status=HTTP_404_NOT_FOUND)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.get(*args, **kwargs)


def custom_500_handler(request, *args, **argv):
    return JsonResponse(
        {"status_code": 500, "message": "Internal Server Error!", "result": None},
        status=500,
    )


class ErrorView(APIView):
    permission_classes = []

    def get(self, *args, **kwargs):
        raise ValueError("This is a test error")
