"""
Django settings for beelearn project.

Generated by "django-admin startproject" using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import json
import os
import dj_database_url
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import firebase_admin
from firebase_admin import credentials

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DNS"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
)

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True #"RENDER" not in os.environ

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS += RENDER_EXTERNAL_HOSTNAME.split(",")

# Application definition
INSTALLED_APPS = [
    "grappelli",
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "debug_toolbar",
    "generic_relations",
    "martor",
    "nested_admin",
    "cloudinary_storage",
    "cloudinary",
    "django_extensions",
    "nested_inline",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "djira.apps.DJiraConfig",
    # apps
    "catalogue.apps.CatalogueConfig",
    "assessment.apps.AssessmentConfig",
    "account.apps.AccountConfig",
    "reward.apps.RewardConfig",
    "payment.apps.PaymentConfig",
    "messaging.apps.MessagingConfig",
    "enhancement.apps.EnhancementConfig",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "beelearn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "beelearn.wsgi.application"
ASGI_APPLICATION = "beelearn.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django_tidb",
    #         "NAME": os.environ.get("DATABASE_NAME"),
    #         "USER": os.environ.get("DATABASE_USER"),
    #         "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
    #         "HOST": os.environ.get("DATABASE_HOST"),
    #         "PORT": "4000",
    #         "OPTIONS": {
    #             "ssl": {
    #                 "ca": "/etc/ssl/certs/ca-certificates.crt",
    #                 "sslmode": "VERIFY_IDENTITY",
    #             }
    #         },
    #     },
    # }
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        ),
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Following settings only make sense on production and may break development environments.
if not DEBUG:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    # STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 8,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "url_filter.integrations.drf.DjangoFilterBackend",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://usebeelearn.com",
    "http://bee-learn.web.app",
    "https://bee-learn.web.app",
    "https://beelearn.onrender.com",
    "http://beelearn.onrender.com",
    "http://academy.usebeelearn.com",
    "https://academy.usebeelearn.com",
]


DJIRA_SETTINGS = {
    "AUTHENTICATION_CLASSES": ["djira.authentication.TokenAuthentication"],
}


CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://*.usebeelearn.com",
]

AUTH_USER_MODEL = "account.user"


cred = credentials.Certificate(
    json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY"))
)

firebase_admin.initialize_app(cred)

CLOUDINARY_STORAGE = {
    "EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS": (),
}


# martor config
MARTOR_ENABLE_ADMIN_CSS = False
MARTOR_IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")
MARTOR_IMGUR_API_KEY = os.environ.get("IMGUR_API_KEY")

# grappelli config

GRAPPELLI_ADMIN_TITLE = "BeeLearn"

# debug toolbar

INTERNAL_IPS = [
    "127.0.0.1",
]

TIME_ZONE = "Africa/Lagos"
