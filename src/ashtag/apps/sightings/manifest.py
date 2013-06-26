from django.core.urlresolvers import reverse

from manifesto.manifest import Manifest


class SightingsManifest(Manifest):
    def cache(self):
        return [
            reverse('sightings:submit'),
        ]
