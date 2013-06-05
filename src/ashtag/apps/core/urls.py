from django.conf.urls import patterns, url

urlpatterns = patterns('ashtag.apps.core.views',
    url(r'^env/$', 'show_env'),
)