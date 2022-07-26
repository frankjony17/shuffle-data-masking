"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

import environ

ROOT = environ.Path(__file__) - 2

ENV = environ.Env(
    DATABASE_NAME=(str, os.environ.get("SHUFFLE_DATA_MASKING_NAME", "SHUFFLE_DATA_MASKING")),
    DATABASE_USER=(str, os.environ.get("SHUFFLE_DATA_MASKING_USER", "svcshuffledatamaskingdsv")),
    DATABASE_PASSWORD=(str, os.environ.get("SHUFFLE_DATA_MASKING_PASSWORD", "Neo@12345AaAaA678")),
    DATABASE_HOST=(str, os.environ.get("SHUFFLE_DATA_MASKING_HOST", "VAWDSQLDB01")),
    DATABASE_PORT=(int, os.environ.get("SHUFFLE_DATA_MASKING_PORT", 1433)),
    FKSOLUTIONS_DATABASE_NAME=(str, os.environ.get("FKSOLUTIONS_NAME", "FKSOLUTIONS")),
    FKSOLUTIONS_DATABASE_USER=(str, os.environ.get("FKSOLUTIONS_USER", "svcpixdsv")),
    FKSOLUTIONS_DATABASE_PASSWORD=(str, os.environ.get("FKSOLUTIONS_PASSWORD", "Neo@12345AaAaA678")),
    FKSOLUTIONS_DATABASE_HOST=(str, os.environ.get("FKSOLUTIONS_HOST", "VAWDSQLDB01")),
    FKSOLUTIONS_DATABASE_PORT=(int, os.environ.get("FKSOLUTIONS_PORT", 1433)),
    FKSOLUTIONS_DATABASE_NAME=(str, os.environ.get("FKSOLUTIONS_NAME", "FKSolutions")),
    FKSOLUTIONS_DATABASE_USER=(str, os.environ.get("FKSOLUTIONS_USER", "svcpixdsv")),
    FKSOLUTIONS_DATABASE_PASSWORD=(str, os.environ.get("FKSOLUTIONS_PASSWORD", "Neo@12345AaAaA678")),
    FKSOLUTIONS_DATABASE_HOST=(str, os.environ.get("FKSOLUTIONS_HOST", "VAWDSQLDB01")),
    FKSOLUTIONS_DATABASE_PORT=(int, os.environ.get("FKSOLUTIONS_PORT", 1433)),
    QUEUE_DATA_MASKING=(str, os.environ.get("QUEUE_DATA_MASKING", "shuffle-data-masking-queue")),
    QUEUE_DATA_MASKING_EXCHANGE=(
        str, os.environ.get("QUEUE_DATA_MASKING_EXCHANGE", "shuffle-data-masking-exchange")),
    QUEUE_DATA_MASKING_HOST=(str, os.environ.get("QUEUE_DATA_MASKING_HOST", "rabbitdev.qadomain.local")),
    QUEUE_DATA_MASKING_PORT=(int, os.environ.get("QUEUE_DATA_MASKING_PORT", 5672)),
    QUEUE_DATA_MASKING_USER=(str, os.environ.get("QUEUE_DATA_MASKING_USER", "fksolutionsAppDev")),
    QUEUE_DATA_MASKING_PASSWORD=(str, os.environ.get("QUEUE_DATA_MASKING_PASSWORD", "rabbitfksolutionsdev")),
)
environ.Env.read_env(str(ROOT.path(".env")))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pol+^yb1cxfz1rj8aqerz&roy$gjg=05wuf^&#!x2vi(vhj6_q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'introspection',
    'datamasking',
    'processerror',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(ROOT.path("main/templates"))]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": ENV("DATABASE_NAME"),
        "USER": ENV("DATABASE_USER"),
        "PASSWORD": ENV("DATABASE_PASSWORD"),
        "HOST":  ENV("DATABASE_HOST"),
        "PORT": ENV("DATABASE_PORT")
    },
    'FKSOLUTIONS': {
        "ENGINE": "mssql",
        "NAME": ENV("FKSOLUTIONS_DATABASE_NAME"),
        "USER": ENV("FKSOLUTIONS_DATABASE_USER"),
        "PASSWORD": ENV("FKSOLUTIONS_DATABASE_PASSWORD"),
        "HOST": ENV("FKSOLUTIONS_DATABASE_HOST"),
        "PORT": ENV("FKSOLUTIONS_DATABASE_PORT")
    },
    'FKSolutions': {
        "ENGINE": "mssql",
        "NAME": ENV("FKSOLUTIONS_DATABASE_NAME"),
        "USER": ENV("FKSOLUTIONS_DATABASE_USER"),
        "PASSWORD": ENV("FKSOLUTIONS_DATABASE_PASSWORD"),
        "HOST": ENV("FKSOLUTIONS_DATABASE_HOST"),
        "PORT": ENV("FKSOLUTIONS_DATABASE_PORT")
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


ALLOWED_HOSTS = ['*']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = [
    str(ROOT.path("main/static"))
]

STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT.path("site_static"))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Queues
QUEUE_DATA_MASKING = ENV("QUEUE_DATA_MASKING")
QUEUE_DATA_MASKING_EXCHANGE = ENV("QUEUE_DATA_MASKING_EXCHANGE")
QUEUE_DATA_MASKING_HOST = ENV("QUEUE_DATA_MASKING_HOST")
QUEUE_DATA_MASKING_PORT = ENV("QUEUE_DATA_MASKING_PORT")
QUEUE_DATA_MASKING_USER = ENV("QUEUE_DATA_MASKING_USER")
QUEUE_DATA_MASKING_PASSWORD = ENV("QUEUE_DATA_MASKING_PASSWORD")
