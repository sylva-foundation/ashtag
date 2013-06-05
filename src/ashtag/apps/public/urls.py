from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('ashtag.apps.public.views',
    url('^$', TemplateView.as_view(template_name='public/home.html'), name='home'),
)