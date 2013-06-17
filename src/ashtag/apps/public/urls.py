from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('ashtag.apps.public.views',
    url('^$', TemplateView.as_view(template_name='public/home.html'), name='home'),
    url('^about/$', TemplateView.as_view(template_name='public/about.html'), name='about'),
    url('^privacy/$', TemplateView.as_view(template_name='public/privacy.html'), name='privacy'),
)