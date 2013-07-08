from django.core.management.base import BaseCommand, CommandError

from ashtag.apps.core.models import Sighting
from ashtag.apps.core.utils import create_thumbnails


class Command(BaseCommand):
    def handle(self, *args, **options):
        total = Sighting.objects.count()
        counter = 1
        for sighting in Sighting.objects.all():
            print "Generating thumbnails for %d of %d ... " % (counter, total),
            if sighting.image:
                create_thumbnails(sighting.image)
                print "done"
            else:
                print "no image, skipping"
            counter += 1
