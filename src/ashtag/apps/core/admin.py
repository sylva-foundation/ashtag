#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from sorl.thumbnail import get_thumbnail

from .models import Sighting, Tree


class SightingAdmin(admin.ModelAdmin):

    list_display = ('created', 'link', 'tree_tag_number', 'thumbnail',
                    'creator_email', 'creator', 'disease_state', 'notes')
    search_fields = ('tree__tag_number',)

    def tree_tag_number(self, obj):
        return obj.tree.tag_number
    tree_tag_number.short_description = 'tree'

    def link(self, obj):
        return """
        <a href="%s">
        See
        </a>""" % (obj.get_absolute_url())
    link.allow_tags = True

    def thumbnail(self, obj):
        im = get_thumbnail(obj.image, '450x270')
        return """
        <a href="%s">
        <img src="%s" width="228px" height="135px"/>
        </a>""" % (obj.image.url, im.url)
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
