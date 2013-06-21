from django.core.urlresolvers import NoReverseMatch, reverse

from manifesto import Manifest as Manifest

from ashtag.apps.public import urls


class PublicManifest(Manifest):

    def cache(self):
        cache_urls = []
        for url in urls.urlpatterns:
            try:
                # Dont cache the home page, as the user
                # presumably already has it in the appcache
                # as the user will have been there. This will
                # also make cache updates easier
                if url.name != 'home':
                    cache_urls.append(reverse('public:%s' % url.name))
            except NoReverseMatch:
                # Probably requires a parameter, in which case move on
                pass

        return cache_urls

    def network(self):
        return [

        ]
