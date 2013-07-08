import sys

from django.core.management.base import BaseCommand

from ashtag.apps.core.models import Sighting
from ashtag.apps.core.utils import create_thumbnails


def _log(s):
    sys.stdout.write(s)
    sys.stdout.flush()


class Command(BaseCommand):
    def handle(self, *args, **options):
        total = Sighting.objects.count()
        counter = 1
        for sighting in Sighting.objects.all():
            _log("Generating thumbnails for %d of %d ... " % (counter, total))
            if sighting.image:
                if create_thumbnails(sighting.image):
                    _log("done\n")
                else:
                    _log("ERRORS (logged)\n")
            else:
                _log("no image, skipping\n")
            counter += 1
