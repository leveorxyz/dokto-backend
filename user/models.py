from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel

# Create your models here.


class User(AbstractUser, CoreModel):
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
        blank=True,
        null=True,
    )
    full_name = models.CharField(_("full name"), max_length=180, blank=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    user_type = models.CharField(
        _("user type"), max_length=20, default="Patient", blank=True
    )
    is_verified = models.BooleanField(
        _("is verified"), default=False, blank=True, null=True
    )
    street = models.CharField(_("street"), max_length=100, blank=True, null=True)
    state = models.CharField(_("state"), max_length=50, blank=True, null=True)
    city = models.CharField(_("city"), max_length=50, blank=True, null=True)
    zip_code = models.CharField(_("zip code"), max_length=15, blank=True, null=True)
    contact_no = models.CharField(_("contact no"), max_length=20, blank=True, null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


class UserIp(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.user.username
