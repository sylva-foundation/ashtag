from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('ashtag.apps.sightings.views',
    url('^$', TemplateView.as_view(template_name='sightings/home.html'), name='home'),
    url('^example/$', TemplateView.as_view(template_name='sightings/example.html'), name='example'),
)