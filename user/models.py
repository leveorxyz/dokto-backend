import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel
from core.literals import (
    PROFILE_PHOTO_DIRECTORY,
    IDENTIFICATION_PHOTO_DIRECTORY,
    DOCTOR_EDUCATION_PHOTO_DIRECTORY,
)

# Create your models here.


class User(AbstractUser, CoreModel):
    class UserType(models.TextChoices):
        ADMIN = "ADMIN", _("admin")
        DOCTOR = "DOCTOR", _("doctor")
        PATIENT = "PATIENT", _("patient")
        PHARMACY = "PHARMACY", _("pharmacy")
        HOSPITAL = "HOSPITAL", _("hospital")

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters and digits only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(_("full name"), max_length=180, blank=True)
    email = models.EmailField(_("email"), unique=True)
    user_type = models.CharField(
        _("user type"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.PATIENT,
        blank=True,
    )
    is_verified = models.BooleanField(
        _("is verified"), default=False, blank=True, null=True
    )
    street = models.CharField(_("street"), max_length=100, blank=True, null=True)
    state = models.CharField(_("state"), max_length=50, blank=True, null=True)
    city = models.CharField(_("city"), max_length=50, blank=True, null=True)
    zip_code = models.CharField(_("zip code"), max_length=15, blank=True, null=True)
    contact_no = models.CharField(_("contact no"), max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to=PROFILE_PHOTO_DIRECTORY,
        blank=True,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserIp(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username}-{self.ip_address}"


class UserLanguage(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}-{self.language}"


class DoctorInfo(CoreModel):
    class Gender(models.TextChoices):
        MALE = "MALE", _("male")
        FEMALE = "FEMALE", _("female")
        OTHER = "OTHER", _("other")

    class IdentificationType(models.TextChoices):
        PASSPORT = "PASSPORT", _("passport")
        DRIVER_LICENSE = "DRIVER'S LICENSE", _("driver's license")
        STATE_ID = "STATE ID", _("state id")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=7, choices=Gender.choices, blank=True, null=True
    )
    identification_type = models.CharField(
        max_length=20, choices=IdentificationType.choices, null=True, blank=True
    )
    identification_number = models.CharField(max_length=50, blank=True, null=True)
    identification_photo = models.ImageField(
        upload_to=IDENTIFICATION_PHOTO_DIRECTORY, blank=True, null=True
    )
    professional_bio = models.TextField(max_length=512, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)


class DoctorEducation(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    course = models.CharField(max_length=50)
    year = models.CharField(max_length=15)
    college = models.CharField(max_length=60)
    certificate = models.ImageField(upload_to=DOCTOR_EDUCATION_PHOTO_DIRECTORY)


class DoctorExperience(CoreModel):
    establishment_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField(max_length=200, blank=True, null=True)


class DoctorSpecialty(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)


class CollectiveInfo(CoreModel):
    class CollectiveType(models.TextChoices):
        HOSPITAL = "HOSPITAL", _("hospital")
        CLINIC = "CLINIC", _("clinic")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collective_type = models.CharField(max_length=20, choices=CollectiveType.choices)
    number_of_practitioners = models.IntegerField(blank=True, null=True, default=0)
