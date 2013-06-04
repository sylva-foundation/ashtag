from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^account/', include('ashtag.apps.account.urls')),
    url(r'^api/', include('ashtag.apps.api.urls')),
    url(r'^core/', include('ashtag.apps.core.urls')),
    url(r'^app/', include('ashtag.apps.sightings.urls')),
    url(r'^/', include('ashtag.apps.public.urls')),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
