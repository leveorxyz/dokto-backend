from django.db import models

from core.models import CoreModel
from user.models import DoctorInfo, PatientInfo, DoctorSpecialty



# Create your models here.


class Appointment(CoreModel):
    """
    Appointment model
    """

    patient = models.ForeignKey(
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
    payment = models.ForeignKey('accounting.Payment', null=True, on_delete=models.CASCADE, related_name='paymentt')
    patient_status = models.CharField(max_length=50, null=True)
    specialty = models.ForeignKey(DoctorSpecialty, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

