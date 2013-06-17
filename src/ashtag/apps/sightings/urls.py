from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('ashtag.apps.sightings.views',
    url('^$', RedirectView.as_view(url='/sightings/my-tags/'), name='home'),
    url('^my-tags/$', TemplateView.as_view(template_name='sightings/my-tags.html'), name='my-tags'),
    url('^list/$', TemplateView.as_view(template_name='sightings/list.html'), name='list'),
    url('^gallery/$', TemplateView.as_view(template_name='sightings/gallery.html'), name='gallery'),
    url('^map/$', TemplateView.as_view(template_name='sightings/map.html'), name='map'),
    url('^submit/$', TemplateView.as_view(template_name='sightings/submit.html'), name='submit'),
    url('^view/(?P<slug>[a-z0-9]+)/$', TemplateView.as_view(template_name='sightings/view.html'), name='view'),
)