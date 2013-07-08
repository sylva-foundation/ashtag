from ashtag.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'database_email_backend',
    'django_nose',
)

EMAIL_BACKEND = 'database_email_backend.backend.DatabaseEmailBackend'

DATABASES = {
    'default': {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "ashtag",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Django Nose
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# Celery
BROKER_URL = 'django://'
INSTALLED_APPS += ['kombu.transport.django']
