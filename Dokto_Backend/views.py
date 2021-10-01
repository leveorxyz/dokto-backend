from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND


class Custom404(APIView):
    def get(self, *args, **kwargs):
        response_data = {
            "message": "Not found!",
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
