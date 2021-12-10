from django.db import models

from core.models import CoreModel
from core.literals import DOCTOR_WAITING_ROOM_MEDIA_DIRECTORY
from user.models import DoctorInfo

# Create your models here.


class WaitingRoom(CoreModel):
    doctor = models.OneToOneField(DoctorInfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    room_media = models.FileField(
        upload_to=DOCTOR_WAITING_ROOM_MEDIA_DIRECTORY, blank=True, null=True
    )
