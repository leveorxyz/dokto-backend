from django.db import models

from core.models import CoreModel
from user.models import DoctorInfo, PatientInfo
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PatientEncounters(CoreModel):
    class Gender(models.TextChoices):
        MALE = "MALE", _("male")
        FEMALE = "FEMALE", _("female")
        OTHER = "OTHER", _("other")

    # username = models.CharField(
    #     _("username"),
    #     max_length=150,
    #     unique=True,
    #     help_text=_("Required. 150 characters or fewer. Letters and digits only."),
    #     validators=[username_validator],
    #     error_messages={
    #         "unique": _("A user with that username already exists."),
    #     },
    # )
    
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)
    provider = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    

    visit_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    visit_reason = models.CharField(max_length=512, blank=True, null=True)
    
    signed = models.BooleanField(blank=True, null=True)

    # gender = models.CharField(
    #     max_length=7, choices=Gender.choices, blank=True, null=True
    # )

class AssessmentDiagnosis(CoreModel):
    class Type(models.TextChoices):
        ACUTE = "ACUTE", _("acute")
        CHRONIC = "CHRONIC", _("chronic")

    patient_encounter = models.ForeignKey(PatientEncounters, on_delete=models.CASCADE)

    icd = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    snomed_code = models.CharField(max_length=100, blank=True, null=True)
    snomed_description = models.CharField(max_length=512, blank=True, null=True)
    disease_name = models.CharField(max_length=256, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    type = models.CharField(
        max_length=25, choices=Type.choices, blank=True, null=True
    )
    primary_diagnosis = models.BooleanField(blank=True, null=True)
    assessment = models.CharField(max_length=512, blank=True, null=True)

class MedicalNotes(CoreModel):
   
    patient_encounter = models.ForeignKey(PatientEncounters, on_delete=models.CASCADE)

    medical_notes = models.TextField() #models.CharField(max_length=1024, blank=True, null=True)
    notes_html = models.TextField(blank=True, null=True)



