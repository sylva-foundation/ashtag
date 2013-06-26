from ashtag.settings.base import *

import json
with open('/home/dotcloud/environment.json') as f:
    env = json.load(f)

DEBUG = bool(env.get('DEBUG', False))
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ashtag',
        'USER': env['DOTCLOUD_DB_SQL_LOGIN'],
        'PASSWORD': env['DOTCLOUD_DB_SQL_PASSWORD'],
        'HOST': env['DOTCLOUD_DB_SQL_HOST'],
        'PORT': int(env['DOTCLOUD_DB_SQL_PORT']),
    }
}

PAYPAL_SANDBOX_MODE = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

EMAIL_HOST = env.get('EMAIL_HOST', None)
EMAIL_HOST_USER = env.get('EMAIL_HOST_USER', None)
EMAIL_PORT = int(env.get('EMAIL_PORT', None))
EMAIL_USE_TLS = bool(env.get('EMAIL_USE_TLS', None))
EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL = env.get('DEFAULT_FROM_EMAIL', None)
OSCAR_FROM_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Raven / sentry
if env.get('RAVEN_DSN', None):
    RAVEN_CONFIG = {
        'dsn': env.get('RAVEN_DSN')
    }

    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]
