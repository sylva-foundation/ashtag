from django.core.urlresolvers import NoReverseMatch, reverse

from manifesto import Manifest as Manifest

from ashtag.apps.public import urls


class PublicManifest(Manifest):

    def cache(self):
        cache_urls = []
        for url in urls.urlpatterns:
            try:
                cache_urls.append(reverse('public:%s' % url.name))
            except NoReverseMatch:
                # Probably requires a parameter, in which case move on
                pass

        return cache_urls

    def network(self):
        return [

        ]
