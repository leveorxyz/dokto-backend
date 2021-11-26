import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from core.models import CoreModel
from core.literals import (
    PROFILE_PHOTO_DIRECTORY,
    DOCTOR_IDENTIFICATION_PHOTO_DIRECTORY,
    DOCTOR_EDUCATION_PHOTO_DIRECTORY,
    DOCTOR_LICENSE_FILE_DIRECTORY,
    PATIENT_IDENTIFICATION_PHOTO_DIRECTORY,
)

# Create your models here.

username_validator = UnicodeUsernameValidator()


class User(AbstractUser, CoreModel):
    class UserType(models.TextChoices):
        ADMIN = "ADMIN", _("admin")
        DOCTOR = "DOCTOR", _("doctor")
        PATIENT = "PATIENT", _("patient")
        PHARMACY = "PHARMACY", _("pharmacy")
        CLINIC = "CLINIC", _("clinic")

    username = None
    first_name = None
    last_name = None
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

    @property
    def token(self):
        try:
            token, _ = Token.objects.get_or_create(user=self)
            return token.key
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token expired.")


class UserIp(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.id}-{self.ip_address}"


class DoctorInfo(CoreModel):
    class Gender(models.TextChoices):
        MALE = "MALE", _("male")
        FEMALE = "FEMALE", _("female")
        OTHER = "OTHER", _("other")
        PREFER_NOT_TO_SAY = "PREFER NOT TO SAY", _("preder not to say")

    class IdentificationType(models.TextChoices):
        PASSPORT = "PASSPORT", _("passport")
        DRIVER_LICENSE = "DRIVER'S LICENSE", _("driver's license")
        STATE_ID = "STATE ID", _("state id")

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=30, choices=Gender.choices, blank=True, null=True
    )
    identification_type = models.CharField(
        max_length=20, choices=IdentificationType.choices, null=True, blank=True
    )
    identification_number = models.CharField(max_length=50, blank=True, null=True)
    identification_photo = models.ImageField(
        upload_to=DOCTOR_IDENTIFICATION_PHOTO_DIRECTORY, blank=True, null=True
    )
    professional_bio = models.TextField(max_length=512, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    awards = models.TextField(max_length=512, blank=True, null=True)
    license_file = models.FileField(
        upload_to=DOCTOR_LICENSE_FILE_DIRECTORY, blank=True, null=True
    )
    notification_email = models.EmailField(blank=True, null=True)
    reason_to_delete = models.CharField(max_length=2000, blank=True, null=True)
    temporary_disable = models.BooleanField(blank=True, default=False)
    accepted_insurance = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.id}-{self.username}"


class DoctorLanguage(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.doctor_info.username}-{self.language}"


class DoctorEducation(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    course = models.CharField(max_length=50)
    year = models.CharField(max_length=15)
    college = models.CharField(max_length=60)
    certificate = models.ImageField(
        upload_to=DOCTOR_EDUCATION_PHOTO_DIRECTORY, null=True, blank=True
    )

    # def delete(self, *args, **kwargs):
    #     """
    #     Deletes the image file in the storage manually before deletion of an instance
    #     """
    #     storage, path = self.certificate.storage, self.certificate.path
    #     super(DoctorEducation, self).delete(*args, **kwargs)
    #     storage.delete(path)


class DoctorExperience(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, default=None)
    establishment_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField(max_length=200, blank=True, null=True)


class DoctorSpecialty(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)


class DoctorAvailableHours(CoreModel):
    class DayOfWeek(models.TextChoices):
        SUNDAY = "SUN", _("sunday")
        MONDAY = "MON", _("monday")
        TUESDAY = "TUE", _("tuesday")
        WEDNESDAY = "WED", _("wednesday")
        THURSDAY = "THU", _("thursday")
        FRIDAY = "FRI", _("friday")
        SATURDAY = "SAT", _("saturday")

    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=3, choices=DayOfWeek.choices, blank=True, null=True
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)


class DoctorReview(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=80, null=True, blank=True)
    star_count = models.FloatField(null=True, blank=True)
    comment = models.TextField(max_length=5000, null=True, blank=True)


class ClinicInfo(CoreModel):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_practitioners = models.IntegerField(blank=True, null=True, default=0)


class PharmacyInfo(CoreModel):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_practitioners = models.IntegerField(blank=True, null=True, default=0)


class PatientInfo(CoreModel):
    class Gender(models.TextChoices):
        MALE = "MALE", _("male")
        FEMALE = "FEMALE", _("female")
        OTHER = "OTHER", _("other")
        PREFER_NOT_TO_SAY = "PREFER NOT TO SAY", _("preder not to say")

    class IdentificationType(models.TextChoices):
        PASSPORT = "PASSPORT", _("passport")
        DRIVER_LICENSE = "DRIVER'S LICENSE", _("driver's license")
        STATE_ID = "STATE ID", _("state id")
        STUDENT_ID = "STUDENT ID", _("student id")

    class InsuranceType(models.TextChoices):
        SELF_PAID = "SELF PAID", _("self paid")
        INSURANCE_VERIFIED = "INSURANCE VERIFIED", _("insurance verified")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    date_of_birth = models.DateField()
    social_security_number = models.CharField(max_length=12, null=True, blank=True)
    identification_type = models.CharField(
        max_length=20, choices=IdentificationType.choices
    )
    identification_number = models.CharField(max_length=50)
    identification_photo = models.ImageField(
        upload_to=PATIENT_IDENTIFICATION_PHOTO_DIRECTORY, blank=True, null=True
    )

    # Insurance Info
    insurance_type = models.CharField(max_length=20, choices=InsuranceType.choices)
    insurance_name = models.CharField(max_length=50, null=True, blank=True)
    insurance_number = models.CharField(max_length=50, null=True, blank=True)
    insurance_policy_holder_name = models.CharField(
        max_length=50, null=True, blank=True
    )

    # Insurance reference
    referring_doctor_full_name = models.CharField(max_length=50, null=True, blank=True)
    referring_doctor_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    referring_doctor_address = models.CharField(max_length=100, null=True, blank=True)
