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
