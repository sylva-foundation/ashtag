#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tastypie.resources import NamespacedModelResource
from tastypie import fields

from ..core.models import Sighting, Tree


class TreeResource(NamespacedModelResource):
    class Meta:
        queryset = Tree.objects.all()
        resource_name = 'tree'
        excludes = ['creator_email']
        allowed_methods = ['get']


class SightingResource(NamespacedModelResource):
    tree = fields.ForeignKey(TreeResource, 'tree', full=True)
    class Meta:
        queryset = Sighting.objects.all()
        resource_name = 'sighting'
        excludes = ['creator_email']
        allowed_methods = ['get']
