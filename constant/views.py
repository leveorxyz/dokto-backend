import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.conf import settings

from core.literals import available_care


class AvailableCare(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        return Response(
            {"status_code": 200, "message": "Success.", "result": available_care}
        )


class Country(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "constant" / "json" / "country.json"))
        return Response({"status_code": 200, "message": "Success.", "result": data})


class State(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "constant" / "json" / "state.json"))
        query_params = self.request.query_params
        if "country_code" not in query_params:
            raise ValidationError("country_code is required.")
        try:
            return Response(
                {
                    "status_code": 200,
                    "message": "Success.",
                    "result": data[query_params["country_code"]],
                }
            )
        except KeyError:
            return Response(
                {"status_code": 404, "message": "Not found.", "result": []}, status=404
            )


class City(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "constant" / "json" / "city.json"))
        query_params = self.request.query_params
        if "country_code" not in query_params and "state_code" not in query_params:
            raise ValidationError("country_code and status_code are required.")
        try:
            return Response(
                {
                    "status_code": 200,
                    "message": "Success.",
                    "result": data[query_params["country_code"]][
                        query_params["state_code"]
                    ],
                }
            )
        except KeyError:
            return Response(
                {"status_code": 404, "message": "Not found.", "result": []}, status=404
            )
