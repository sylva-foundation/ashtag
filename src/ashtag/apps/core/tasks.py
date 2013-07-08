from celery import task

from .utils import create_thumbnails as create_thumbnails_util
from .models import Sighting


@task()
def create_thumbnails(imageField):
    create_thumbnails_util(imageField)


@task()
def create_all_thumbnails():
    for sighting in Sighting.objects.all():
        create_thumbnails.delay(sighting.image)
