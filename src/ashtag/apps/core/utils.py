from uuid import uuid4


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
