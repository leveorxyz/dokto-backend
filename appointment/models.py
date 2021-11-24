from django.db import models

from core.models import CoreModel
from user.models import DoctorInfo, PatientInfo

# Create your models here.


class Appointment(CoreModel):
    """
    Appointment model
    """

    patient = models.OneToOneField(
        PatientInfo, on_delete=models.CASCADE, related_name="patient_appointment"
    )
    doctor = models.ForeignKey(
        DoctorInfo, on_delete=models.CASCADE, related_name="doctor_appointment"
    )
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    number_of_patients = models.IntegerField(default=0)
    payment_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    patient_status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title
