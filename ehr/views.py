from django.db.models.fields import mixins
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, logout

from core.views import CustomRetrieveAPIView, CustomCreateAPIView
from core.utils import set_user_ip
from ehr.models import (MedicalNotes, PatientEncounters,AssessmentDiagnosis)
from user.models import User, PatientInfo
from user.serializers import (
    UserSerializer,
    PatientRegistrationSerializer,
)
from .serializers import (AssessmentDiagnosisSerializer, MedicalNotesSerializer, PatientEncounterSerializer, PatientSerializer)
# Create your views here.


class AllEncounters(ListCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter endpoint

        Request method: POST

        Request fields
        ---
        - patient: uuid
        - provider: uuid
        - visit_date: string
        - location: string
        - visit_reason: string
        - signed: boolean

    """    
    queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PatientEncounters(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PatientEncounters.objects.all()
    serializer_class = PatientEncounterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AssessmentDiagnosisView(ListCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient assesment and diagnosis endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
        

    """    
    queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AssessmentDiagnosisUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)





class MedicalNotesView(ListCreateAPIView):
    permission_classes = [AllowAny]
    """
        Patient encounter medical notes endpoint

        Request method: POST

        Request fields
        ---
        - patient_encounter: uuid
        

    """    
    queryset = MedicalNotes.objects.all()
    serializer_class = MedicalNotesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




class MedicalNotesUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = AssessmentDiagnosis.objects.all()
    serializer_class = AssessmentDiagnosisSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)







#@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# class AllEncounters1(ListCreateAPIView):
#     """
#     List all code patientEncounter, or create a new snippet.
#     """
#     def get(self, request, *args, **kwargs):
#         #if request.method == 'GET':
#         patientEncounter = PatientEncounters.objects.all()
#         serializer = PatientEncounterSerializer(patientEncounter, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     def post(self, request, *args, **kwargs):
#         data = JSONParser().parse(request)
#         serializer = PatientEncounterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @csrf_exempt
# def PatientEncountersFun(request, pid):
#     """
#     List all code patientEncounter, or create a new snippet.
#     """
#     if request.method == 'GET':
#         patientEncounter = PatientEncounters.objects.get(provider_id=pid)
#         serializer = PatientEncounterSerializer(patientEncounter, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PatientEncounterSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)



# @csrf_exempt
# def PatientEncounterDetails(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         patientEncounter = PatientEncounters.objects.get(pk=pk)
#     except PatientEncounters.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PatientEncounterSerializer(patientEncounter)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PatientEncounterSerializer(patientEncounter, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         patientEncounter.delete()
#         return HttpResponse(status=204)



# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def hello_world(request):
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     elif request.method == 'PUT':
#         return Response({"message": "Got some data!", "data": request.data})
#     elif request.method == 'GET':
#         return Response({"message": "Got some data!", "data": request.data})
#     elif request.method == 'DELETE':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})


