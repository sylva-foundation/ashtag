# Django settings for ashtag project.

import os
from oscar.defaults import *
from path import path
from oscar import OSCAR_MAIN_TEMPLATE_DIR

PROJECT_ROOT = path(__file__).dirname().abspath().realpath().parent.parent.parent
APPS_ROOT = PROJECT_ROOT / 'src' / 'ashtag' / 'apps'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Adam Charnock', 'adam@adamcharnock.com'),
    ('Steve Pike', 'ashtag@stevepike.co.uk'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'GMT'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_ROOT / 'static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT / 'assets',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

FIXTURE_DIRS = (
    PROJECT_ROOT / 'fixtures',
)

# Pull the SECRET_KEY from the environment.
if os.environ.get('DJANGO_SECRET_KEY'):
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.Emailbackend',
    'django.contrib.auth.backends.ModelBackend',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',

    'ashtag.apps.core.context_processors.enable_tracking',
    'ashtag.apps.core.context_processors.image_sizes',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'ashtag.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT / 'templates',
    OSCAR_MAIN_TEMPLATE_DIR,
    # This is a trick (i.e. a hack) for django-oscar-paypal to allow
    # us to override oscar's templates more easily
    # (See http://django-oscar-paypal.readthedocs.org/en/latest/express.html)
    path(OSCAR_MAIN_TEMPLATE_DIR).parent,
)

from oscar import get_core_apps as oscar_get_core_apps
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.gis',
    # 'django.contrib.admindocs',

    'ashtag.apps.api',
    'ashtag.apps.core',
    'ashtag.apps.public',
    'ashtag.apps.sightings',
    'ashtag.apps.store',

    'django_extensions',
    'pipeline',
    'south',
    'registration',
    'storages',
    'tastypie',
    'tz_detect',
    'manifesto',
    'djcelery',

    # oscar
    'compressor',
    'paypal',
] + oscar_get_core_apps(['ashtag.apps.oscar.shipping'])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# Pipeline configuration
STATICFILES_STORAGE = 'ashtag.apps.core.storages.PipelineForgivingStorage'
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

# Compressor (used for Oscar's UIs, which are not public, so disable it)
COMPRESS_ENABLED = False

# Django registration etc
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
LOGIN_REDIRECT_URL = 'sightings:my-tags'

# Oscar
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}
# Check for a sensible flow before enabling this
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_PARTNER_WRAPPERS = {
    'adapt': 'ashtag.apps.store.partnerwrappers.AdaptWrapper',
}
# Tax percentage as string (0.2 = 20%).
# Used in ashtag.apps.store.partnerwrappers.AdaptWrapper, not by Oscar core code
OSCAR_TAX = '0.2'

# Oscar PayPal
PAYPAL_API_USERNAME = os.environ.get('PAYPAL_API_USERNAME', 'not-set')
PAYPAL_API_PASSWORD = os.environ.get('PAYPAL_API_PASSWORD', 'not-set')
PAYPAL_API_SIGNATURE = os.environ.get('PAYPAL_API_SIGNATURE', 'not-set')
PAYPAL_CURRENCY = "GBP"
PAYPAL_ALLOW_NOTE = False

# Manifesto
MANIFESTO_EXCLUDED_MANIFESTS = 'pipeline.manifest.PipelineManifest'
MANIFESTO_VERSIONER = 'manifesto.versioners.FileContentsVersioner'
MANIFESTO_FILTER = 'manifesto.filters.ExcludePatternFilter'
MANIFESTO_FILTER_EXCLUDE_PATTERNS = [
    "^%soscar" % STATIC_URL,
    "^%sadmin" % STATIC_URL,
    "\.less$",
    "\.coffee$",
    "/errors/.*\.html$",
    '/\.DS_Store$',
    'images/guide/',
    '/treebeard/',
    '/django_extensions/',
    '/robots.txt$',
    '/favicon.ico$',
]

# File storage configuration

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'ashtag-localdev')
AWS_HEADERS = {
    'Cache-Control': 'max-age=31536000, public',
}

if os.environ.get('AWS_MEDIA_ENABLE', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

if os.environ.get('AWS_STATIC_ENABLE', False):
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Image sizes
# (We define these here so we can pre-generate them)
IMAGE_SIZES = {
    'admin': '228x135',
    'large': '750x600',
    'thumb': '150x150',
}

# Tracking switch
ENABLE_TRACKING_CODE = bool(os.environ.get('ENABLE_TRACKING_CODE', False))

# Celery
import djcelery
djcelery.setup_loader()

from ashtag.settings.assets import *
