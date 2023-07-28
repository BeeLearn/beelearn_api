"""
Django settings for beelearn project.

Generated by "django-admin startproject" using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default = "django-insecure-f&4h0n2)4t1)0*3*6^eo^1^*ww+-3ui$odqw+zkupnu$l_ti#j")
# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["beelearn.onrender.com", "*"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

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
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "djira.apps.DJiraConfig",
    # apps
    "catalogue.apps.CatalogueConfig",
    "account.apps.AccountConfig",
    "reward.apps.RewardConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "beelearn.urls"

TEMPLATES = [{
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
else :
    DATABASES = {
        "default": {
            "ENGINE": "django_tidb",
            "NAME": os.environ.get("DATABASE_NAME", default = "django"),
            "USER": os.environ.get("DATABASE_USER",default = "root"),
            "PASSWORD": os.environ.get("DATABASE_PASSWORD", default = ""),
            "HOST": os.environ.get("DATABASE_HOST", default = "localhost"),
            "PORT": "4000",
            "OPTIONS": {
                "ssl": {
                    "ca": "/etc/secrets/cert.pem",
                    "sslmode": "VERIFY_IDENTITY",
                }
            }
        },
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{
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

if DEBUG:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 8,
    "DEFAULT_FILTER_BACKENDS": ["url_filter.integrations.drf.DjangoFilterBackend"],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:55288",
]


DJIRA_SETTINGS = {
    "AUTHENTICATION_CLASSES": ["djira.authentication.TokenAuthentication"],
}