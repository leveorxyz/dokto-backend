import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, ValidationError
from django.conf import settings
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiExample,
    extend_schema,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes

from core.views import CustomAPIView


class AvailableCare(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[OpenApiExample(name="example 1", value=["string"])],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "available_care.json"))
        return Response({"status_code": 200, "message": "Success.", "result": data})


class Country(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[{"name": "string", "country_code": "string"}],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "country.json"))
        return Response({"status_code": 200, "message": "Success.", "result": data})


class State(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter("country_code", str, required=True),
        ],
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[{"name": "string", "state_code": "string"}],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "state.json"))
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

    @extend_schema(
        parameters=[
            OpenApiParameter("country_code", str, required=True),
            OpenApiParameter("state_code", str, required=True),
        ],
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[OpenApiExample(name="example 1", value=["string"])],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "city.json"))
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


class PhoneCode(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[{"name": "string", "phone_code": "string"}],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "country_phone_code.json"))
        return Response({"status_code": 200, "message": "Success.", "result": data})


class AcceptedInsurance(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=["string"],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "accepted_insurance.json"))
        return Response({"status_code": 200, "message": "Success.", "result": data})


class ProfessionView(CustomAPIView):
    permission_classes = (AllowAny,)
    http_method_names = ["get", "options"]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[{"name": "string", "profession_code": "string"}],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, request, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "professions.json"))
        return super().get(request, response_data=data, *args, **kwargs)


class ServicesView(CustomAPIView):
    permission_classes = (AllowAny,)
    http_method_names = ["get", "options"]

    @extend_schema(
        parameters=[
            OpenApiParameter("profession_code", str, required=True),
        ],
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[OpenApiExample(name="example 1", value=["string"])],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, request, *args, **kwargs):
        data = json.load(open(settings.BASE_DIR / "json" / "profession_services.json"))
        query_params = self.request.query_params
        if "profession_code" not in query_params:
            raise ValidationError("profession_code is required.")
        try:
            service_data = data[query_params["profession_code"]]
            return super().get(request, response_data=service_data, *args, **kwargs)
        except KeyError:
            return Response(
                {"status_code": 404, "message": "Not found.", "result": []}, status=404
            )
