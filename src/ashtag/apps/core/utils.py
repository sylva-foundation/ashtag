from uuid import uuid4

from sorl.thumbnail import get_thumbnail

from django.conf import settings


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

def create_thumbnails(imageField):
    for size in settings.IMAGE_SIZES.values():
        get_thumbnail(imageField, size)
