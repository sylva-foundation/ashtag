from django.core.urlresolvers import reverse

from manifesto.manifest import Manifest


class PublicManifest(Manifest):
    def cache(self):
        return [
            reverse('public:home'),
        ]
