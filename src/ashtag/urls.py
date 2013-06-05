from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^account/', include('ashtag.apps.account.urls', namespace='account', app_name='account')),
    url(r'^api/', include('ashtag.apps.api.urls', namespace='api', app_name='api')),
    url(r'^core/', include('ashtag.apps.core.urls', namespace='core', app_name='core')),
    url(r'^app/', include('ashtag.apps.sightings.urls', namespace='sightings', app_name='sightings')),
    url(r'^', include('ashtag.apps.public.urls', namespace='public', app_name='public')),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
