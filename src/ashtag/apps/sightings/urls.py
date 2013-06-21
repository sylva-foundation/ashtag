from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from ashtag.apps.sightings.views import *

urlpatterns = patterns('ashtag.apps.sightings.views',
    url('^$', RedirectView.as_view(url='/sightings/my-tags/'), name='home'),

    url('^my-tags/$', login_required(MyTagsView.as_view()), name='my-tags'),
    url('^list/$', ListView.as_view(), name='list'),
    url('^gallery/$', GalleryView.as_view(), name='gallery'),
    url('^map/$', MapView.as_view(), name='map'),
    url('^submit/$', SubmitView.as_view(), name='submit'),
    url('^sent/$', SentView.as_view(), name='sent'),
    url('^tree/(?P<identifier>[a-z0-9]+)/$', TreeView.as_view(), name='tree'),
    url('^tree/(?P<identifier>[a-z0-9]+)/flag/$', FlagView.as_view(), name='flag'),

)
