"""
Django settings for django_file_upload project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from decouple import config, Csv
from django.urls import reverse_lazy
from django_jinja.builtins import DEFAULT_EXTENSIONS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from google.oauth2 import service_account

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_DIR = os.path.realpath(os.path.join(BASE_DIR, '..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^8sg7bzv^iyvhr3+u&d@7&frskh1lw%4g6c-r1i=*3b2f_f@c8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       default='localhost', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_framework',

    'django_file_upload.upload',
    'django_file_upload.core',
    'django_file_upload.capacity',
    'django_file_upload.confirmation',
    'django_file_upload.users',

    'django_jinja',
    'drf_yasg',
    'raven.contrib.django.raven_compat',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_file_upload.urls'

_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
]


TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            # Use jinja2/ for jinja jinja2
            "app_dirname": "jinja2",
            # Don't figure out which template loader to use based on
            # file extension
            "match_extension": "",
            "auto_reload": DEBUG,
            "context_processors": _CONTEXT_PROCESSORS,
            # 'extensions': DEFAULT_EXTENSIONS + [
            #     'pipeline.jinja2.PipelineExtension',
            # ],
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': _CONTEXT_PROCESSORS,
}
    },
]

WSGI_APPLICATION = 'django_file_upload.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEFAULT_DATABASE = config('DATABASE_URL',
                          default='postgres://postgres:root@localhost:5432/postgres',
                          cast=dj_database_url.parse)

DATABASES = {
    'default': DEFAULT_DATABASE
}

# DATABASES = {
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.sqlite3',
#     #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     # }
#
#     'default': {
#         'NAME': 'sq_uploads',
#         'ENGINE': 'django.db.backends.postgresql',
#         'USER': 'postgres',
#         'PASSWORD': 'root',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Celery settings
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/files/'

MEDIA_DIR = os.path.realpath(os.path.join(HOME_DIR, 'media/'))

STATIC_ROOT = os.path.join(BASE_DIR, "static_files")
MEDIA_ROOT = os.path.join(BASE_DIR, "media_files")

RELATIVE_FILE_PATH = "service-account-key.json"

print(os.path.isfile(RELATIVE_FILE_PATH))

if os.path.isfile(RELATIVE_FILE_PATH):
    print("Found file")
    with open(RELATIVE_FILE_PATH, "r") as f:
        print(f.read())

if os.path.isfile(RELATIVE_FILE_PATH):
    print("With GS Credentials")
    GS_BUCKET_NAME = 'sq-django-uploads'
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        RELATIVE_FILE_PATH
    )
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'django_file_upload.custom_storages.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'django_file_upload.custom_storages.MediaStorage'

else:
    print("No GS Credentials")
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

LOGIN_REDIRECT_URL = reverse_lazy('auth:dashboard')
AUTH_USER_MODEL = 'users.User'

RAVEN_CONFIG = {
    'dsn': config('SENTRY_DSN_URL', default=None),
}
