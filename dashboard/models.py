from django.db import models

from core.models import CoreModel
from user.models import ClinicInfo, DoctorInfo

# Create your models here.


class HospitalTeam(CoreModel):
    clinic = models.ForeignKey(ClinicInfo, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100, null=True, blank=True)


class HospitalService(CoreModel):
    clinic = models.ForeignKey(ClinicInfo, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100, null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
