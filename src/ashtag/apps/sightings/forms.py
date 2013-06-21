#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from decimal import Decimal

from django import forms

from exifpy import EXIF

from ashtag.apps.core.models import Sighting, Tree
from .exif_utils import get_lat_lon


class SightingForm(forms.ModelForm):
    tag_number = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Sighting
        exclude = ('id', 'tree', 'created', 'modified', 'creator_email')

    def __init__(self, user, *args, **kwargs):
        super(SightingForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        """Sort out the tag number"""
        c_data = self.cleaned_data

        c_data['tree'] = None
        tag_number = c_data.get('tag_number')
        if tag_number:
            try:
                c_data['tree'] = Tree.objects.get(
                    tag_number=tag_number)
            except Tree.DoesNotExist:
                if self.user.is_authenticated():
                    # Then we can make a new tagged tree and attribute it to
                    # this user. ADAPT will verify.
                    c_data['tree'] = Tree.objects.create(
                        location=c_data.get('location'),
                        creator_email=self.user.email,
                        tag_number=tag_number
                    )
                else:
                    self._errors["tag_number"] = self.error_class([(
                        "Hey! It looks like we haven't seen this tag number "
                        "yet. If you are trying to claim it, please log in "
                        "first!")])
        else:
            c_data['tree'] = Tree.objects.create(
                location=c_data.get('location'),
                creator_email=self.user.email
                if self.user.is_authenticated()
                else c_data['creator_email']
            )

        return c_data


class AnonSightingForm(SightingForm):
    """Wraps up sightings by non-auth'd users."""

    class Meta:
        model = Sighting
        exclude = ('id', 'tree', 'created', 'modified')
