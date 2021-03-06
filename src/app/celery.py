import os

import environ
from celery import Celery
from django.conf import settings

__all__ = [
    "celery",
]

env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

celery = Celery("app")

celery.config_from_object(settings.CELERY)

celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # noqa E800
