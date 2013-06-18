from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from ashtag.apps.sightings.views import *

urlpatterns = patterns('ashtag.apps.sightings.views',
    url('^$', RedirectView.as_view(url='/sightings/my-tags/'), name='home'),

    url('^my-tags/$', MyTagsView.as_view(), name='my-tags'),
    url('^list/$', ListView.as_view(), name='list'),
    url('^gallery/$', GalleryView.as_view(), name='gallery'),
    url('^map/$', MapView.as_view(), name='map'),
    url('^submit/$', SubmitView.as_view(), name='submit'),
    url('^view/(?P<pk>[a-z0-9]+)/$', SightingView.as_view(), name='view'),
)
