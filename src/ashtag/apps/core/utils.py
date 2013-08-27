from uuid import uuid4
import logging

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError

from django.conf import settings

logger = logging.getLogger('ashtag.apps.core.utils')


def pk_generator(length=6):
    """Create a unique pk string consisting of 0-9a-z."""
    long_pk = (
        uuid4().bytes
        .encode('base64')
        .rstrip('=\n')
        .replace('/', '')
        .replace('+', '')
        .lower()
    )
    return long_pk[:length]


def create_thumbnails(image_field):
    errors = False
    for size_name, size in settings.IMAGE_SIZES.items():
        try:
            get_thumbnail(image_field, size, **settings.IMAGE_OPTIONS[size_name])
        except (IOError, ThumbnailError):
            errors = True
            logger.exception("Failed to create thumbnail")
    return not errors
