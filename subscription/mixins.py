# Create your models here.

from django.db import models
from user.models import User


UserType = User.UserType

class SubscriptionUserTypes(models.TextChoices):
    DOCTOR = UserType.DOCTOR
    CLINIC = UserType.CLINIC
    PHARMACY = UserType.PHARMACY

