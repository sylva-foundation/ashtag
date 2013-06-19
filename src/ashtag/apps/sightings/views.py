import json

from django.views.generic import TemplateView, DetailView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import mail_managers

from ashtag.apps.core.models import Tree, Sighting

from .forms import SightingForm, AnonSightingForm
from .utils import email_owner


FLAGGED_MESSAGE = """
Dear ADAPT,

Someone has flagged {3}:

    {0}

You can hide it or un-flag it here:

    {1}

The flagger's email address is: {2}

Have a good day!

"""


SIGHTING_MESSAGE = """
Dear AshTag Tagger,

An update was posted to your Tagged Tree #{0}!

You can see the update here:

    {1}

Please note, if the update is not for your tree, you can flag the update and it
will be removed.

Have a good day!

"""


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
            if sighting.tree.creator_email != request.user.email:
                email_owner(
                    sighting.tree,
                    "Update on your Tree!",
                    SIGHTING_MESSAGE.format(
                        sighting.tree.tag_number,
                        sighting.get_absolute_url()
                    )
                )
            return redirect('sightings:sent')
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)

        # set template context here

        return context


class SentView(TemplateView):
    template_name = 'sightings/thanks.html'


class TreeView(DetailView):
    """Summary page for a particular tree."""
    queryset = Tree.objects.exclude(hidden=True)
    template_name = 'sightings/view.html'

    def get_object(self):
        try:
            return self.queryset.get(tag_number=self.kwargs['tag_number'])
        except Tree.DoesNotExist:
            raise Http404

    def post(self, request, tag_number):
        """Allow the creator to send updates, make changes etc."""
        tree = self.get_object()

        kwargs = request.POST
        result = {}

        # Update the exemplar sighting:
        if 'exemplar' in kwargs:
            if request.user != tree.creator:
                raise PermissionDenied

            exemplar_id = kwargs['exemplar']
            try:
                sighting = tree.sighting_set.get(id=exemplar_id)
            except Sighting.DoesNotExist:
                raise Http404
            tree.exemplar = sighting
            tree.save()
            result['exemplar'] = {
                'message': 'OK',
                'location': tree.get_absolute_url(),
            }

        # Flag the Tree
        if 'flag_tree' in kwargs:
            # just mail managers to deal with it
            tree.flagged = True
            tree.save()
            mail_managers(
                "Tagged Tree was flagged!",
                FLAGGED_MESSAGE.format(
                    tree.get_absolute_url(),
                    reverse('admin:core_tree_change', args=[tree.id]),
                    request.user.email
                    if request.user.is_authenticated()
                    else 'anonymous',
                    "a tree"
                )
            )
            result['flag_tree'] = {
                'message': 'OK',
                'flag': tree.id,
            }

        # Flag a sighting
        if 'flag_update' in kwargs:
            flag_update = kwargs['flag_update']
            try:
                sighting = tree.sighting_set.get(id=flag_update)
            except Sighting.DoesNotExist:
                raise Http404

            if request.user == tree.creator:
                # remove this straight away.
                sighting.hidden = True
                sighting.flagged = True
                sighting.save()
                result['flag_update'] = {
                    'message': 'OK',
                    'remove': flag_update,
                }
            else:
                # set a flag, and maybe alert the owner/ADAPT
                sighting.flagged = True
                sighting.save()
                mail_managers(
                    "Update was flagged",
                    FLAGGED_MESSAGE.format(
                        tree.get_absolute_url(),
                        reverse('admin:core_sighting_change', args=[sighting.id]),
                        request.user.email
                        if request.user.is_authenticated()
                        else 'anonymous',
                        "an update"
                    ),
                    fail_silently=True)
                result['flag_update'] = {
                    'message': 'OK',
                    'flag': flag_update,
                }

        return HttpResponse(
            json.dumps(result), content_type="application/json; charset=utf-8")

    def get_context_data(self, **kwargs):
        context = super(TreeView, self).get_context_data(**kwargs)
        context['updates'] = self.object.sighting_set.exclude(hidden=True)
        context['tagged'] = self.object.tag_number

        return context
