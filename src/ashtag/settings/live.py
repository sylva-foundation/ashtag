from ashtag.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ENV['MYSQLS_DATABASE'],
        'USER': ENV['MYSQLS_USERNAME'],
        'PASSWORD': ENV['MYSQLS_PASSWORD'],
        'HOST': ENV['MYSQLS_HOSTNAME'],
        'PORT': ENV['MYSQLS_PORT']
    }
}

PAYPAL_SANDBOX_MODE = False

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

EMAIL_HOST = ENV.get('EMAIL_HOST', None)
EMAIL_HOST_USER = ENV.get('EMAIL_HOST_USER', None)
EMAIL_PORT = int(ENV.get('EMAIL_PORT', None))
EMAIL_USE_TLS = bool(ENV.get('EMAIL_USE_TLS', None))
EMAIL_HOST_PASSWORD = ENV.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL = ENV.get('DEFAULT_FROM_EMAIL', None)
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
if ENV.get('RAVEN_DSN', None):
    RAVEN_CONFIG = {
        'dsn': ENV.get('RAVEN_DSN')
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
BROKER_URL = ENV['REDISCLOUD_URL']
