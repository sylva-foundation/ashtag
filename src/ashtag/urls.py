from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.contrib import admin
admin.autodiscover()
admin.site.login = login_required(admin.site.login)

from ashtag.apps.core.views import AshTagRegistrationView
from oscar.app import application as oscar_application

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/adam/Projects/ashtag/static'}),

    # We extend the default RegistrationView
    url(r'^accounts/register/$', AshTagRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^tz-detect/', include('tz_detect.urls')),
    url(r'^', include('manifesto.urls')),

    url(r'^accounts/', include('registration.backends.simple.urls', app_name='registration')),
    url(r'^api/', include('ashtag.apps.api.urls', namespace='api', app_name='api')),
    url(r'^core/', include('ashtag.apps.core.urls', namespace='core', app_name='core')),
    url(r'^sightings/', include('ashtag.apps.sightings.urls', namespace='sightings', app_name='sightings')),

    url(r'^store/checkout/paypal/', include('paypal.express.urls')),
    url(r'^store/o/', include(oscar_application.urls)),
    url(r'^store/', include('ashtag.apps.store.urls', namespace='store', app_name='store')),

    url(r'^', include('ashtag.apps.public.urls', namespace='public', app_name='public')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
