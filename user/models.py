from __future__ import annotations

from django.db import models, transaction, IntegrityError
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from core.classes import ExpiringActivationTokenGenerator
from core.models import CoreModel
from core.literals import (
    PROFILE_PHOTO_DIRECTORY,
    DOCTOR_IDENTIFICATION_PHOTO_DIRECTORY,
    DOCTOR_LICENSE_FILE_DIRECTORY,
    PATIENT_IDENTIFICATION_PHOTO_DIRECTORY,
    CLINIC_LICENSE_FILE_DIRECTORY,
    PHARMACY_LICENSE_FILE_DIRECTORY,
)
from core.modelutils import send_mail
from .utils import generate_file_and_name

# Create your models here.

username_validator = UnicodeUsernameValidator()


class PasswordResetWhitelist(CoreModel):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, unique=True)


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
    country = models.CharField(max_length=50, blank=True, null=True, default=None)
    contact_no = models.CharField(_("contact no"), max_length=20, blank=True, null=True)
    _profile_photo = models.ImageField(
        upload_to=PROFILE_PHOTO_DIRECTORY,
        blank=True,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @classmethod
    def from_validated_data(cls, validated_data: dict):
        fields = [field.name for field in User._meta.fields]

        validated_data["password"] = make_password(validated_data.pop("password"))
        constructor_kwargs = {
            field: validated_data.pop(field)
            for field in fields
            if field in validated_data
        }
        return cls(**constructor_kwargs)

    @classmethod
    def get_hidden_fields(self) -> list:
        return super().get_hidden_fields() + [
            "is_staff",
            "is_superuser",
            "is_verified",
            "_profile_photo",
            "is_active",
            "date_joined",
        ]

    @property
    def token(self):
        try:
            token, _ = Token.objects.get_or_create(user=self)
            return token.key
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token expired.")

    @property
    def profile_photo(self):
        domain = Site.objects.get_current().domain
        if self._profile_photo.name:
            return domain + self._profile_photo.url

    @profile_photo.setter
    def profile_photo(self, profile_photo_data):
        if self._profile_photo.name:
            del self.profile_photo
        file_name, file = generate_file_and_name(profile_photo_data, self.id)
        self._profile_photo.save(file_name, file, save=True)
        self.save()

    @profile_photo.deleter
    def profile_photo(self):
        if self._profile_photo.name:
            self._profile_photo.delete(save=True)

    def delete(self, *args, **kwargs):
        del self.profile_photo
        return super(User, self).delete(*args, **kwargs)

    def send_email_verification_mail(self):
        template = "email/account_verification.html"

        confirmation_token = ExpiringActivationTokenGenerator().generate_token(
            text=self.email
        )

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "email-verification",
                ]
            )
            + f"?token={confirmation_token.decode('utf-8')}"
        )
        send_mail(
            to_email=self.email,
            subject=f"Welcome to Dokto, please verify your email address",
            template_name=template,
            input_context={
                "name": self.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )

    def send_password_reset_mail(self):

        template = "email/password_reset.html"

        reset_token = ExpiringActivationTokenGenerator().generate_token(text=self.email)

        try:
            _ = PasswordResetWhitelist.objects.create(
                email=self.email, token=reset_token.decode("utf-8")
            )
        except IntegrityError:
            raise ValidationError("Password reset mail is already sent.")

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "password-reset",
                ]
            )
            + f"?token={reset_token.decode('utf-8')}"
        )
        send_mail(
            to_email=self.email,
            subject=f"Dokto Password Reset",
            template_name=template,
            input_context={
                "name": self.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )

    @classmethod
    def verify_password_reset(cls, token: str, password: str) -> None:
        user = None
        whitelist_token = None
        try:
            whitelist_token = PasswordResetWhitelist.objects.get(token=token)
        except PasswordResetWhitelist.DoesNotExist:
            raise ValidationError("Invalid token.")
        email = ExpiringActivationTokenGenerator().get_token_value(token)

        try:
            user = cls.objects.get(email=email)
        except cls.DoesNotExist:
            raise ValidationError("Invalid token.")

        user.set_password(password)
        user.save()
        whitelist_token.delete()

    def get_username(self) -> str:
        if (
            self.user_type == User.UserType.PATIENT
            or self.user_type == User.UserType.ADMIN
        ):
            return None
        user_type_map = {
            User.UserType.DOCTOR: "doctor_info",
            User.UserType.PHARMACY: "pharmacy_info",
            User.UserType.CLINIC: "clinic_info",
        }
        return getattr(self, user_type_map[self.user_type]).username

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return self.email


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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_info"
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=30, choices=Gender.choices, blank=True, null=True
    )
    identification_type = models.CharField(
        max_length=20, choices=IdentificationType.choices, null=True, blank=True
    )
    identification_number = models.CharField(max_length=50, blank=True, null=True)
    _identification_photo = models.ImageField(
        upload_to=DOCTOR_IDENTIFICATION_PHOTO_DIRECTORY, blank=True, null=True
    )
    professional_bio = models.TextField(max_length=512, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    awards = models.TextField(max_length=512, blank=True, null=True)
    _license_file = models.FileField(
        upload_to=DOCTOR_LICENSE_FILE_DIRECTORY, blank=True, null=True
    )
    notification_email = models.EmailField(blank=True, null=True)
    reason_to_delete = models.CharField(max_length=2000, blank=True, null=True)
    temporary_disable = models.BooleanField(blank=True, default=False)
    accepted_insurance = models.CharField(max_length=100, blank=True, null=True)
    license_expiration = models.DateField(blank=True, null=True)

    @classmethod
    def get_hidden_fields(self, *args, **kwargs) -> list:
        return super().get_hidden_fields() + [
            "_identification_photo",
            "_license_file",
            "id",
            "user",
            "reason_to_delete",
            "temporary_disable",
            "notification_email",
        ]

    @property
    def rating(self):
        rating = self.doctorreview_set.all().aggregate(models.Avg("star_count"))[
            "star_count__avg"
        ]
        return rating if rating else 0

    @property
    def review_count(self):
        return len(self.doctorreview_set.all())

    @property
    def identification_photo(self):
        domain = Site.objects.get_current().domain
        if self._identification_photo.name:
            return domain + self._identification_photo.url

    @identification_photo.setter
    def identification_photo(self, identification_photo_data):
        if self._identification_photo.name:
            del self.identification_photo
        file_name, file = generate_file_and_name(identification_photo_data, self.id)
        self._identification_photo.save(file_name, file, save=True)
        self.save()

    @identification_photo.deleter
    def identification_photo(self):
        if self._identification_photo.name:
            self._identification_photo.delete(save=True)

    @property
    def license_file(self):
        domain = Site.objects.get_current().domain
        if self._license_file.name:
            return domain + self._license_file.url

    @license_file.setter
    def license_file(self, license_file_data):
        if self._license_file.name:
            del self.license_file
        file_name, file = generate_file_and_name(license_file_data, self.id)
        self._license_file.save(file_name, file, save=True)
        self.save()

    @license_file.deleter
    def license_file(self):
        if self._license_file.name:
            self._license_file.delete(save=True)

    def delete(self, *args, **kwargs):
        del self.identification_photo
        del self.license_file
        return super(DoctorInfo, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.username}"


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


class DoctorExperience(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, default=None)
    establishment_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField(max_length=200, blank=True, null=True)


class DoctorSpecialty(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50, null=True)
    price = models.IntegerField(help_text="Input amount in cents")


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


class DoctorAcceptedInsurance(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    insurance = models.CharField(max_length=50)


class DoctorProfession(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)


class DoctorService(CoreModel):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    price = models.CharField(max_length=50)


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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="clinic_info"
    )
    number_of_practitioners = models.IntegerField(blank=True, null=True, default=0)
    notification_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, default=None)
    _license_file = models.FileField(
        upload_to=CLINIC_LICENSE_FILE_DIRECTORY, blank=True, null=True, default=None
    )
    license_expiration = models.DateField(blank=True, null=True)

    @property
    def license_file(self):
        domain = Site.objects.get_current().domain
        if self._license_file.name:
            return domain + self._license_file.url

    @license_file.setter
    def license_file(self, license_file_data):
        if self._license_file.name:
            del self.license_file
        file_name, file = generate_file_and_name(license_file_data, self.id)
        self._license_file.save(file_name, file, save=True)
        self.save()

    @license_file.deleter
    def license_file(self):
        if self._license_file.name:
            self._license_file.delete(save=True)

    def delete(self, *args, **kwargs):
        del self.license_file
        return super(ClinicInfo, self).delete(*args, **kwargs)

    def send_onboard_mail(self, doctor_id=None, *args, **kwargs):
        if not doctor_id:
            raise ValidationError("doctor_id is required")
        doctor_user: User = None
        try:
            doctor_user = DoctorInfo.objects.get(id=doctor_id).user
        except DoctorInfo.DoesNotExist:
            raise ValidationError("doctor_id is not valid")
        invite_token = ExpiringActivationTokenGenerator().generate_token(
            text=self.email
        )
        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "onboard",
                ]
            )
            + f"?token={invite_token.decode('utf-8')}"
        )
        send_mail(
            to_email=doctor_user.email,
            subject=f"Dokto doctor onboarding",
            template_name="email/password_reset.html",
            input_context={
                "name": doctor_user.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )

    @classmethod
    def get_hidden_fields(cls):
        return super().get_hidden_fields() + [
            "user",
            "notification_email",
            "website",
            "_license_file",
            "license_expiration",
        ]


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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="pharmacy_info"
    )
    number_of_practitioners = models.IntegerField(blank=True, null=True, default=0)
    notification_email = models.EmailField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    website = models.URLField(blank=True, null=True, default=None)
    _license_file = models.FileField(
        upload_to=PHARMACY_LICENSE_FILE_DIRECTORY, blank=True, null=True, default=None
    )
    license_expiration = models.DateField(blank=True, null=True)

    @property
    def services(self):
        return self.pharmacyservice_set.all().values_list("service", flat=True)

    @property
    def hours_of_operation(self):
        return self.pharmacyavailablehours_set.all().values(
            "day_of_week", "start_time", "end_time"
        )

    @property
    def license_file(self):
        domain = Site.objects.get_current().domain
        if self._license_file.name:
            return domain + self._license_file.url

    @license_file.setter
    def license_file(self, license_file_data):
        if self._license_file.name:
            del self.license_file
        file_name, file = generate_file_and_name(license_file_data, self.id)
        self._license_file.save(file_name, file, save=True)
        self.save()

    @license_file.deleter
    def license_file(self):
        if self._license_file.name:
            self._license_file.delete(save=True)

    def delete(self, *args, **kwargs):
        del self.license_file
        return super(PharmacyInfo, self).delete(*args, **kwargs)

    @classmethod
    def get_hidden_fields(cls):
        return super().get_hidden_fields() + [
            "user",
            "notification_email",
            "bio",
            "website",
            "_license_file",
            "license_expiration",
        ]


class PharmacyService(CoreModel):
    pharmacy_info = models.ForeignKey(PharmacyInfo, on_delete=models.CASCADE)
    service = models.CharField(max_length=200)


class PharmacyAvailableHours(CoreModel):
    class DayOfWeek(models.TextChoices):
        SUNDAY = "SUN", _("sunday")
        MONDAY = "MON", _("monday")
        TUESDAY = "TUE", _("tuesday")
        WEDNESDAY = "WED", _("wednesday")
        THURSDAY = "THU", _("thursday")
        FRIDAY = "FRI", _("friday")
        SATURDAY = "SAT", _("saturday")

    pharmacy_info = models.ForeignKey(PharmacyInfo, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=3, choices=DayOfWeek.choices, blank=True, null=True
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)


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
        SELF_PAY = "SELF-PAY", _("self-pay")
        INSURANCE = "INSURANCE", _("insurance")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    date_of_birth = models.DateField()
    identification_type = models.CharField(
        max_length=20, choices=IdentificationType.choices
    )
    identification_number = models.CharField(max_length=50)
    _identification_photo = models.ImageField(
        upload_to=PATIENT_IDENTIFICATION_PHOTO_DIRECTORY, blank=True, null=True
    )

    display_id = models.PositiveIntegerField(default=1)

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
    name_of_parent = models.CharField(max_length=100, blank=True, null=True)
    notification_email = models.EmailField(blank=True, null=True)

    @classmethod
    def get_hidden_fields(cls):
        return super().get_hidden_fields() + [
            "_identification_photo",
            "user",
            "id",
            "display_id",
            "notification_email",
        ]

    @property
    def identification_photo(self):
        domain = Site.objects.get_current().domain
        if self._identification_photo.name:
            return domain + self._identification_photo.url

    @identification_photo.setter
    def identification_photo(self, identification_photo_data):
        if self._identification_photo.name:
            del self.identification_photo
        file_name, file = generate_file_and_name(identification_photo_data, self.id)
        self._identification_photo.save(file_name, file, save=True)
        self.save()

    @identification_photo.deleter
    def identification_photo(self):
        if self._identification_photo.name:
            self._identification_photo.delete(save=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = PatientInfo.objects.all().aggregate(
                largest=models.Max("display_id")
            )["largest"]
            if last_id is not None:
                self.display_id = last_id + 1

        super(PatientInfo, self).save(*args, **kwargs)
