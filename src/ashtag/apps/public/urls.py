from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('ashtag.apps.public.views',
    url('^$', TemplateView.as_view(template_name='public/home.html'), name='home'),
    url('^about/$', TemplateView.as_view(template_name='public/about.html'), name='about'),
    url('^contact/$', TemplateView.as_view(template_name='public/contact.html'), name='contact'),
    url('^privacy/$', TemplateView.as_view(template_name='public/privacy.html'), name='privacy'),
    url('^terms/$', TemplateView.as_view(template_name='public/terms.html'), name='terms'),
)