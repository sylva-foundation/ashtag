from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ashtag.apps.core.views import AshTagRegistrationView

urlpatterns = patterns('',
    # We extend the default RegistrationView
	url(r'^accounts/register/$', AshTagRegistrationView.as_view(), name='registration_register'),

    url(r'^accounts/', include('registration.backends.simple.urls', app_name='registration')),
    url(r'^api/', include('ashtag.apps.api.urls', namespace='api', app_name='api')),
    url(r'^core/', include('ashtag.apps.core.urls', namespace='core', app_name='core')),
    url(r'^app/', include('ashtag.apps.sightings.urls', namespace='sightings', app_name='sightings')),
    url(r'^', include('ashtag.apps.public.urls', namespace='public', app_name='public')),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
