from django.conf.urls import patterns, include, url

from ashtag.apps.store.views import TagPacksView

urlpatterns = patterns('',
    url('^tag-packs/$', TagPacksView.as_view(), name="tagpacks")
)
