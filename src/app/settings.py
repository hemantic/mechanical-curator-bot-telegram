import os
from pathlib import Path

import environ

root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file
SITE_ROOT = root()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Disable built-in ./manage.py test command in favor of pytest
TEST_RUNNER = "app.test.disable_test_command_runner.DisableTestCommandRunner"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)
CI = env("CI", cast=bool, default=False)

DEBUG_PROPAGATE_EXCEPTIONS = env("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = ["*"]  # host validation is not necessary in 2021


# Application definition

INSTALLED_APPS = [
    "app",
    "adapters",
    "telegrambot",
    "foods",
    # "levels",
    "users",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"
AUTH_USER_MODEL = "users.User"

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

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    "default": env.db(),
}


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

LANGUAGE_CODE = "en"
LOCALE_PATHS = ["locale"]
TIME_ZONE = env("TIME_ZONE", cast=str, default="Europe/Moscow")
USE_L10N = True
USE_i18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", cast=str, default="static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
# https://docs.djangoproject.com/en/3.1/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "telegrambot": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", cast=str)

BACKEND_URL = env("BACKEND_URL", cast=str)


# Celery conf

CELERY = {
    "broker_url": env("REDIS_URL"),
    "broker_transport_options": {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
        "visibility_timeout": 3600 * 48,
    },
    "result_backend": env("REDIS_URL"),
    "redis_max_connections": env("CELERY_REDIS_MAX_CONNECTIONS", cast=int, default=5),
    "task_always_eager": env("CELERY_ALWAYS_EAGER", cast=bool, default=True),
    "task_reject_on_worker_lost": env(
        "CELERY_TASK_REJECT_ON_WORKER_LOST", cast=bool, default=True
    ),
    "timezone": TIME_ZONE,
    "enable_utc": False,
}


# Fatsecret conf
FATSECRET = {
    "consumer_key": env("FATSECRET_CONSUMER_KEY"),
    "consumer_secret": env("FATSECRET_CONSUMER_SECRET"),
}
