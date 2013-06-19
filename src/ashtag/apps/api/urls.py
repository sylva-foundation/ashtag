from django.conf.urls import patterns, include

from tastypie.api import NamespacedApi

from .api import SightingResource, TreeResource


v1_api = NamespacedApi(api_name='v1', urlconf_namespace='api')
v1_api.register(TreeResource())
v1_api.register(SightingResource())

urlpatterns = patterns(
    '',
    (r'', include(v1_api.urls)),
)
