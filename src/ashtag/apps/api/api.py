#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from tastypie.resources import NamespacedModelResource
from tastypie import fields

from ashtag.apps.core.models import Sighting, Tree


class LatLngMixin(object):
    """Methods to dehydrate lat/lng"""
    def dehydrate_latlng(self, bundle):
        """Get the latlng."""
        return list(reversed(list(bundle.obj.location.get_coords())))


class TreeResource(LatLngMixin, NamespacedModelResource):
    latlng = fields.ListField()
    updates = fields.ToManyField(
        'ashtag.apps.api.api.SightingResource', 'sighting_set')
    view_url = fields.CharField()

    class Meta:
        queryset = Tree.objects.all()
        resource_name = 'tree'
        excludes = ['creator_email', 'location']
        allowed_methods = ['get']

    def dehydrate_view_url(self, bundle):
        """Get the view url for this tree."""
        return bundle.obj.get_absolute_url()


class SightingResource(LatLngMixin, NamespacedModelResource):
    latlng = fields.ListField()
    tree = fields.ForeignKey(TreeResource, 'tree')

    class Meta:
        queryset = Sighting.objects.all()
        resource_name = 'sighting'
        excludes = ['creator_email', 'location']
        allowed_methods = ['get']


class MarkerResource(LatLngMixin, NamespacedModelResource):
    """A slimmed down Tree resource to only give bare minimum data for the map"""
    latlng = fields.ListField()
    view_url = fields.CharField()
    disease_state = fields.CharField()

    class Meta:
        queryset = Tree.objects.select_related('display_sighting').all()
        resource_name = 'marker'
        fields = ['latlng', 'view_url', 'tag_number', 'disease_state']
        allowed_methods = ['get']
        include_resource_uri = False

    def dehydrate_view_url(self, bundle):
        """Get the view url for this tree."""
        return bundle.obj.get_absolute_url()

    def dehydrate_disease_state(self, bundle):
        if bundle.obj.display_sighting:
            state = bundle.obj.display_sighting.disease_state
        else:
            state = None
        return state
