from rest_framework import serializers

from .models import AssessmentDiagnosis, MedicalNotes, PatientEncounters


class PatientEncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientEncounters
        fields = "__all__"


class AssessmentDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentDiagnosis
        fields = "__all__"


class MedicalNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalNotes
        fields = "__all__"
