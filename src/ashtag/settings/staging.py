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

EMAIL_SUBJECT_PREFIX = '[staging]'

EMAIL_HOST = env.get('EMAIL_HOST', None)
EMAIL_HOST_USER = env.get('EMAIL_HOST_USER', None)
EMAIL_PORT = int(env.get('EMAIL_PORT', None))
EMAIL_USE_TLS = bool(env.get('EMAIL_USE_TLS', None))
EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL = env.get('DEFAULT_FROM_EMAIL', None)
OSCAR_FROM_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# This is the suggested dotcloud logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/supervisor/django.log',
            'maxBytes': 1024*1024*25, # 25 MB
            'backupCount': 5,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'ashtag.request': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'log_file'],
            'level': 'INFO',
            'propagate': True,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'log_file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# Raven / sentry
if env.get('RAVEN_DSN', None):
    RAVEN_CONFIG = {
        'dsn': env.get('RAVEN_DSN')
    }

    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

    LOGGING['root']['handlers'] = ['sentry']
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }

# SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PORT', '443')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Celery
BROKER_URL = env.get('DOTCLOUD_REDIS_REDIS_URL')
