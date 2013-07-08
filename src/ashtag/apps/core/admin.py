#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.core.urlresolvers import reverse
from django.conf import settings

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError

from .models import Sighting, Tree


def get_thumbnail_html(image):
    try:
        im = get_thumbnail(image, settings.IMAGE_SIZES['admin'])
    except IOError as e:
        return "IOError: %s" % e
    except ThumbnailError as e:
        return "ThumbnailError: %s" % e

    return """
    <a href="%s">
    <img src="%s" width="228px" height="135px"/>
    </a>""" % (image.url, im.url)


class SightingAdmin(gis_admin.GeoModelAdmin):
    list_display = ('created', 'link', 'tree_tag_number',
                    'creator_email', 'creator', 'disease_state', 'notes', 'thumbnail')
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
        return get_thumbnail_html(obj.image)
    thumbnail.allow_tags = True

    def reject(self, request, queryset):
        for sighting in queryset:
            pass
            # TODO: logic for removing a sighting
#            sighting.save()
#            sighting_rejected.send(sender=self, sighting=sighting)
    reject.short_description = "Mark as rejected"


class TreeAdmin(gis_admin.GeoModelAdmin):
    search_fields = ('tag_number',)
    list_display = ('tag_number', 'id', 'link', 'tag_checked_by', 'creator_email', 'thumbnail')
    actions = ('verify_tag', 'reject_tag')
    list_display_links = ('tag_number', 'id')

    def link(self, obj):
        return """
        <a href="{0}">
        See
        </a>""".format(obj.get_absolute_url())
    link.allow_tags = True

    def thumbnail(self, obj):
        return get_thumbnail_html(obj.image)
    thumbnail.allow_tags = True

    def verify_tag(self, request, queryset):
        for tree in queryset:
            tree.tag_checked_by = request.user
            tree.save()
    verify_tag.short_description = "Verify this tag number"

    def reject_tag(self, request, queryset):
        for tree in queryset:
            tree.tag_checked_by = request.user
            tree.tag_number = None
            tree.save()
    reject_tag.short_description = "Reject this tag number"


admin.site.register(Sighting, SightingAdmin)
admin.site.register(Tree, TreeAdmin)
