#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.core.urlresolvers import reverse

from sorl.thumbnail import get_thumbnail

from .models import Sighting, Tree


class SightingAdmin(gis_admin.GeoModelAdmin):

    list_display = ('created', 'link', 'tree_tag_number', 'thumbnail',
                    'creator_email', 'creator', 'disease_state', 'notes')
    search_fields = ('tree__tag_number',)

    def tree_tag_number(self, obj):
        return """
        <a href="{0}">{1}</a>
        """.format(
            reverse('admin:core_tree_change', args=[obj.tree.id]),
            obj.tree.tag_number or obj.tree.id)
    tree_tag_number.short_description = 'tree'
    tree_tag_number.allow_tags = True

    def link(self, obj):
        return """
        <a href="{0}">
        See
        </a>""".format(obj.get_absolute_url())
    link.allow_tags = True

    def thumbnail(self, obj):
        im = get_thumbnail(obj.image, '450x270')
        return """
        <a href="{0}">
        <img src="{1}" width="228px" height="135px"/>
        </a>""".format(obj.image.url, im.url)
    thumbnail.allow_tags = True

    def reject(self, request, queryset):
        for sighting in queryset:
            pass
            # TODO: logic for removing a sighting
#            sighting.save()
#            sighting_rejected.send(sender=self, sighting=sighting)
    reject.short_description = "Mark as rejected"


admin.site.register(Sighting, SightingAdmin)
admin.site.register(
    Tree, search_fields=('tag_number',), list_display=('id', 'tag_number'))
