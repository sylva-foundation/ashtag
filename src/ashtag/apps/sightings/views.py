import json
import base64

from StringIO import StringIO

from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import TemplateView, DetailView, ListView
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import mail_managers
from django.db.models import Q

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


class MyTagsView(ListView):
    """Shows all my trees, that haven't been hidden by admin."""
    template_name = 'sightings/my-tags.html'

    def get_queryset(self):
        trees = Tree.objects.filter(
            hidden=False,
            creator_email=self.request.user.email)
        trees = sorted(trees, key=lambda t: (bool(t.tag_number), t.created), reverse=True)
        return trees


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

    def get_FILES(self, data, filename):
        """Returns a MultiValueDict with the file image."""
        result = MultiValueDict()
        _data = data[5:]
        _content_type, _b64 = _data.split(';')
        _b64_prefix, _b64 = _b64.split(',')
        _image = base64.b64decode(_b64)
        file_size = len(_image)
        result['image'] = InMemoryUploadedFile(
            file=StringIO(_image),
            field_name='image',
            name=filename,
            content_type=_content_type,
            size=file_size,
            charset=None,
        )
        return result

    def get(self, request, *args, **kwargs):
        form = self._get_form_class(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form_class = self._get_form_class(request)
        files = None
        if not request.FILES and request.POST.get('image_name', False):
            files = self.get_FILES(request.POST.get('image'), request.POST.get('image_name'))
        else:
            files = request.FILES

        form = form_class(request.user, request.POST, files)
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


class TreeGetterMixin(object):
    """Tree could be got by ID or Tag Number."""
    queryset = Tree.objects.exclude(hidden=True)

    def get_object(self):
        try:
            return self.queryset.get(
                Q(tag_number=self.kwargs['identifier']) |
                Q(id=self.kwargs['identifier']))
        except Tree.DoesNotExist:
            raise Http404
        except Tree.MultipleObjectsReturned:
            # TODO: are we sure that a tag number will never be same as id?
            mail_managers(
                "Clashing Tree Tag number/IDs!",
                "ID/Tag was: {0}...".format(self.kwargs['identifier']))
            raise Http404


class FlagView(TreeGetterMixin, DetailView):
    """Called to flag a tree or update."""

    def post(self, request, identifier):
        """Allow the creator to send updates, make changes etc."""
        tree = self.get_object()

        kwargs = request.POST
        result = {}

        # Flag the Tree
        if 'tree' in kwargs:
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
            result['tree'] = {
                'message': 'OK',
                'flag': tree.id,
            }

        # Flag a sighting
        if 'sighting' in kwargs:
            flag_sighting = kwargs['sighting']
            try:
                sighting = tree.sighting_set.get(id=flag_sighting)
            except Sighting.DoesNotExist:
                raise Http404

            if request.user == tree.creator:
                # remove this straight away.
                sighting.hidden = True
                sighting.flagged = True
                sighting.save()
                result['sighting'] = {
                    'message': 'OK',
                    'remove': flag_sighting,
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
                result['sighting'] = {
                    'message': 'OK',
                    'flag': flag_sighting,
                }

        return HttpResponse(
            json.dumps(result), content_type="application/json; charset=utf-8")


class TreeView(TreeGetterMixin, DetailView):
    """Summary page for a particular tree."""
    template_name = 'sightings/view.html'

    def get_context_data(self, **kwargs):
        context = super(TreeView, self).get_context_data(**kwargs)
        context['updates'] = self.object.sighting_set.exclude(hidden=True)
        context['tagged'] = self.object.tag_number

        return context
