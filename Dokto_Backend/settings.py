"""
Django settings for Dokto_Backend project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import ugettext_lazy as _
from decouple import config
from dj_database_url import parse as db_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY", "django-insecure-z8l(0jnbqgj*j^x@^c%xgw80#@=2l_12qqloi(9ij9vfi(yir"
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)
TEMPLATE_DEBUG = DEBUG
VERSION = config("VERSION", "v1")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party Apps,
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework.authtoken",
    "debug_toolbar",
    # Project Apps
    "core",
    "accounting",
    "user",
    "dashboard",
    "twilio_chat",
    "constant",
    "ehr",
    "appointment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Dokto_Backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Dokto_Backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3"),
        cast=db_url,
    )
}

AUTH_USER_MODEL = "user.User"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LOCALE_PATHS = [BASE_DIR / "locale"]

LANGUAGES = (("en", _("English")),)

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Extra settings
USE_X_FORWARDED_HOST = True
SITE_ID = 1

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

FRONTEND_URL = config("FRONTEND_URL", "https://doktoapp.toybethdev.net/#")

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000"
# ]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.classes.CustomTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Dokto API",
    "DESCRIPTION": "Dokto API documentation",
    "VERSION": VERSION,
}

USER_AUTH_TOKEN_EXPIRATION_SECONDS = 3600 * 24 * 30

INTERNAL_IPS = [
    "127.0.0.1",
]
BACKEND_URL = config("BACKEND_URL", "http://127.0.0.1:8000")
FERNET_KEY = config("FERNET_KEY", "MnMxhswjMy2vpJOt9B1qSS8ZZNZ8WTr5Pet3UePaLQU=")

# Stripe Credenentials
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_4eC39HqLyjWDarjtT1zdp7dc")
STRIPE_PUBLISHABLE_KEY = os.getenv(
    "STRIPE_PUBLISHABLE_KEY", "pk_test_TYooMQauvdEDq54NiTphI7jx"
)

PAYSTACK_SECRET_KEY = os.getenv(
    "PAYSTACK_SECRET_KEY", "sk_test_131a38e1f5bcbca8f338e5762118922ea6fc1e92"
)
FLUTTERWAVE_PUBLIC_KEY = os.getenv(
    "FLUTTERWAVE_PUBLIC_KEY", "FLWPUBK_TEST-cef158ec1b1213690fbeeccb930be993-X"
)
FLUTTERWAVE_SECRET_KEY = os.getenv(
    "FLUTTERWAVE_SECRET_KEY", "FLWSECK_TEST-623211fbda02200d0d3b8904bdd27088-X"
)
FLUTTERWAVE_ENCRYPTION_KEY = os.getenv(
    "FLUTTERWAVE_ENCRYPTION_KEY", "FLWSECK_TEST6207416b757f"
)

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID", "AC9bc2f694a5f9034e7ee972e69ee865d8"
)
TWILIO_API_KEY = os.getenv("TWILIO_API_KEY", "SKc6c3595b92ee19b21596509fc6fc92ac")
TWILIO_API_SECRET = os.getenv("TWILIO_API_SECRET", "ailiJJeASuRZu7nggDkT9hyoOKBDYN9m")
TWILIO_CONVERSATION_SERVICE_SID = os.getenv(
    "TWILIO_CONVERSATION_SERVICE_ID", "IS9a972e4c9e51450dbb01e279a8884198"
)
