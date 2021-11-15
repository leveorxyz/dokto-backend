from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from core.literals import available_care


class AvailableCare(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        return Response(
            {"status_code": 200, "message": "Success.", "result": available_care}
        )
