import json
import base64

from StringIO import StringIO
import logging

from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from ashtag.apps.core.models import Tree, Sighting, EmailTemplate, Survey
from ashtag.apps.core.tasks import create_thumbnails

from .forms import SightingForm, AnonSightingForm, ClaimForm

logger = logging.getLogger('ashtag.apps.sightings.views')

class MyTagsView(ListView):
    """Shows all my trees, that haven't been hidden by admin."""
    template_name = 'sightings/my-tags.html'

    def get_queryset(self):
        trees = Tree.objects.filter(
            hidden=False,
            creator_email=self.request.user.email)
        trees = sorted(trees, key=lambda t: (bool(t.tag_number), t.created), reverse=True)
        return trees


class ListView(ListView):
    template_name = 'sightings/list.html'

    def get_queryset(self):
        trees = Tree.objects.filter(hidden=False).exclude(sighting=None).select_related()
        trees = sorted(trees, key=lambda t: t.sighting_set.latest().created, reverse=True)
        return trees

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

    def _save_survey(self, request, sighting):
        fields = ('symptoms', 'tree_size', 'environment', 'num_nearby_trees', 'nearby_disease_state')

        # Create a survey instance and populate its fields
        survey = Survey()
        survey.sighting = sighting
        for field in fields:
            name = 'survey_%s' % field
            if field == 'symptoms':
                # survey_symptoms can have multiple values
                value = dict(request.POST.lists()).get(name, [])
            else:
                value = request.POST.get(name, '')
            setattr(survey, field, value)

        # Ensure values fall within the available choices
        survey.enforce_choices()

        # If all the fields are empty, then don't save it
        empty = True
        for field in fields:
            if getattr(survey, field):
                empty = False
                break

        if empty:
            return None
        else:
            survey.save()
            return survey

    def get_context_data(self, **kwargs):
        context = {
            'symptoms': Survey.SYMPTOMS,
            'tree_sizes': Survey.TREE_SIZES,
            'environments': Survey.ENVIRONMENTS,
            'num_nearby_trees': Survey.NUM_NEARBY_TREES,
            'nearby_disease_state': Survey.NEARBY_DISEASE_STATE,
            'form': self._get_form_class(self.request),
        }
        context.update(kwargs)
        return context

    # def get(self, request, *args, **kwargs):
    #     form = self._get_form_class(request)
    #     return render(request, self.template_name, {'form': form})

    def post(self, request):
        self.request = request

        form_class = self._get_form_class(request)
        files = None
        if not request.FILES and request.POST.get('image_name', False):
            files = self.get_FILES(request.POST.get('image'), request.POST.get('image_name'))
        else:
            files = request.FILES

        form = form_class(request, request.user, request.POST, files)
        if form.is_valid():
            sighting = form.save(commit=False)

            if request.user.is_authenticated():
                sighting.creator_email = request.user.email
            sighting.tree = form.cleaned_data['tree']

            duplicate = sighting.is_duplicate()
            if duplicate:
                # It is a duplicate, so lets just pretend we just saved 
                # the original (and ignore the unsaved sighting we have here)
                if sighting.tree.sighting_set.count() == 0:
                    sighting.tree.delete()
                return self.success_response(request, duplicate)
            
            sighting.save()

            self._save_survey(request, sighting)

            # Create the thumbnails as a background task
            create_thumbnails.delay(sighting.image)
            if sighting.tree.creator_email != sighting.creator_email:
                EmailTemplate.send('new_sighting_to_owner',
                    to_emails=[sighting.tree.creator_email],
                    sighting=sighting,
                    request=request,
                )

            return self.success_response(request, sighting)
        else:
            return render(request, self.template_name, self.get_context_data(form=form))

    def success_response(self, request, sighting):
        if request.is_ajax():
            return HttpResponse('OK')
        else:
            url = "%s?tree=%s" % (reverse('sightings:sent'), sighting.tree.id)
            return redirect(url)


class ClaimView(FormView):
    template_name = 'sightings/claim.html'
    form_class = ClaimForm

    def get_success_url(self):
        return reverse('sightings:tree', args=[self.kwargs['id']])

    def get_form_kwargs(self):
        kwargs = super(ClaimView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['tree'] = get_object_or_404(Tree, id=self.kwargs['id'])
        return kwargs

    def form_valid(self, form):
        tree = get_object_or_404(Tree, id=self.kwargs['id'])
        Sighting.objects.create(
            tree=tree,
            creator_email=form.user.email,
            notes="I claimed this tree!",
            image=form.files['image'],
            location=tree.location,
        )
        tree.tag_number = form.data['tag_number']
        tree.save()
        EmailTemplate.send('admin_new_tag',
            tree=tree,
            request=self.request,
            this_tree_was='claimed from a previous sighting',
        )

        return super(ClaimView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClaimView, self).get_context_data(**kwargs)
        context['tree'] = get_object_or_404(Tree, id=self.kwargs['id'])

        return context


class SentView(TemplateView):
    template_name = 'sightings/thanks.html'

    def get_context_data(self, **kwargs):
        context = super(SentView, self).get_context_data(**kwargs)
        tree = get_object_or_404(Tree, id=self.request.GET.get('tree'))
        context['tree'] = tree
        return context


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
            logger.exception('Clashing Tree Tag number/IDs')
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
            EmailTemplate.send('admin_flagged',
                request=request,
                obj=tree,
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
                EmailTemplate.send('admin_flagged',
                    request=request,
                    obj=sighting,
                )
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
        sightings = self.object.sighting_set.exclude(hidden=True)

        sighting_pk = self.request.GET.get('sighting', None)
        display_sighting = None
        if sighting_pk:
            try:
                display_sighting = sightings.get(pk=sighting_pk)
            except Sighting.DoesNotExist:
                pass

        if not display_sighting:
            display_sighting = self.object.display_sighting

        context['updates'] = sightings
        context['tagged'] = self.object.tag_number
        context['display_sighting'] = display_sighting

        return context
