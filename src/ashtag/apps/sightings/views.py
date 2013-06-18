from django.views.generic import TemplateView, DetailView
from ashtag.apps.core.models import Sighting


class MyTagsView(TemplateView):
    template_name = 'sightings/my-tags.html'

    def get_context_data(self, **kwargs):
        context = super(MyTagsView, self).get_context_data(**kwargs)

        # set template context here

        return context


class ListView(TemplateView):
    template_name = 'sightings/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        # set template context here

        return context


class GalleryView(TemplateView):
    template_name = 'sightings/gallery.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)

        # set template context here

        return context


class MapView(TemplateView):
    template_name = 'sightings/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)

        # set template context here

        return context


class SubmitView(TemplateView):
    template_name = 'sightings/submit.html'

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        # set template context here

        return context


class SightingView(DetailView):
    model = Sighting
    template_name = 'sightings/views.html'

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        # set template context here

        return context
