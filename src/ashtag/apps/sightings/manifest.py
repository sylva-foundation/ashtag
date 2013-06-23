from manifesto import Manifest as Manifest
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from ashtag.apps.core.models import Tree


class SightingsManifest(Manifest):

    def set_key(self, key):
        super(SightingsManifest, self).set_key(key)
        self.key = int(key)
        self.user = User.objects.get(pk=self.key)

    def cache(self):
        urls = [
            reverse('sightings:submit'),
#            reverse('sightings:my-tags'),
#            reverse('sightings:list'),
#            reverse('sightings:gallery'),
#            reverse('sightings:map'),
        ]

        if self.key:
            trees = Tree.objects.filter(creator_email=self.user.email)[:10]
            urls += [t.get_absolute_url() for t in trees]

        return urls

    def network(self):
        return [

        ]
