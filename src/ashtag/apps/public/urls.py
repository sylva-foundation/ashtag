from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import AuthStatusView, PhoneGapView

urlpatterns = patterns('ashtag.apps.public.views',
    url('^$', TemplateView.as_view(template_name='public/home.html'), name='home'),
    url('^about/$', TemplateView.as_view(template_name='public/about.html'), name='about'),
    url('^contact/$', TemplateView.as_view(template_name='public/contact.html'), name='contact'),
    url('^cookies/$', TemplateView.as_view(template_name='public/cookies.html'), name='cookies'),
    url('^terms/$', TemplateView.as_view(template_name='public/terms.html'), name='terms'),
    url('^dieback-identification-guide/$', TemplateView.as_view(template_name='public/guide.html'), name='guide'),
    url('^tagging-video-guide/$', TemplateView.as_view(template_name='public/tagging-video.html'), name='tagging-video'),
    url('^session-status/$', AuthStatusView.as_view(), name='session-status'),
    url('^phonegap/$', PhoneGapView.as_view(), name='phonegap'),
)
