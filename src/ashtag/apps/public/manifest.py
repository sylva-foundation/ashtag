from hashlib import sha1

from django.core.urlresolvers import reverse
from django.conf import settings

from manifesto.manifest import Manifest


class PublicManifest(Manifest):
    def cache(self):
        return [
            reverse('public:home'),
            '/static/images/ashtaglogo.png',
        ]

    def version_data(self):
        templates = [
            settings.PROJECT_ROOT / 'templates' / 'public' / 'home.html',
            settings.PROJECT_ROOT / 'templates' / 'sightings' / 'submit.html',
            settings.PROJECT_ROOT / 'templates' / 'core' / 'ashtag-base.html',
            settings.PROJECT_ROOT / 'templates' / 'core' / 'jqm-page.html',
            settings.PROJECT_ROOT / 'templates' / 'core' / 'includes' / 'footer.html',
            settings.PROJECT_ROOT / 'templates' / 'core' / 'includes' / 'menu.html',
        ]
        version_data = []
        for path in templates:
            with open(path) as t:
                hash_ = sha1(t.read()).hexdigest()
                version_data.append(hash_)
        return version_data
