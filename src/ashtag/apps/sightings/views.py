from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect

from ashtag.apps.core.models import Sighting

from .forms import SightingForm, AnonSightingForm


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
    form_class = SightingForm

    def _get_form_class(self, request):
        if not request.user.is_authenticated():
            return AnonSightingForm
        else:
            return SightingForm

    def get(self, request, *args, **kwargs):
        form = self._get_form_class(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form_class = self._get_form_class(request)
        form = form_class(request.user, request.POST, request.FILES)
        if form.is_valid():
            sighting = form.save(commit=False)
            if request.user.is_authenticated():
                sighting.creator_email = request.user.email
            sighting.tree = form.cleaned_data['tree']
            sighting.save()
            return redirect('sightings:sent')
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        # set template context here

        return context


class SentView(TemplateView):
    template_name = 'sightings/thanks.html'


class SightingView(DetailView):
    model = Sighting
    template_name = 'sightings/views.html'

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        # set template context here

        return context
