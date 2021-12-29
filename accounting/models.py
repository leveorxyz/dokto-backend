from django.db import models
from core.models import CoreModel
from appointment.models import Appointment

# Create your models here.
class Payment(CoreModel):
    amount_paid = models.IntegerField()
    transaction_reference = models.TextField() # or Charfield(max-lneght) SESSION id AS TRANSACTION REF FOR STRIPE
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appointment')
    paid = models.BooleanField(default=False)
    payment_gateway = models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return self.transaction_reference
