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
        """Do some work to get EXIF, locations etc."""
        c_data = self.cleaned_data
        exif = None
        try:
            f = c_data['image'].file
            f.seek(0)
            exif = EXIF.process_file(f)
            # weird little hack for some vals are malformatted...
            for i in exif.items():
                try:
                    str(i)
                except:
                    exif[i[0]] = i[1].printable
        except Exception, e:
            logging.error(e)
            exif = None

        if not c_data.get('location') and exif:
            # there's exif and no location given
            lat, lon = get_lat_lon(exif)
            if lat and lon:
                location = "SRID=4326;POINT(%s %s)"
                c_data['location'] = location % (
                    Decimal(str(lon)), Decimal(str(lat)))
            else:
                msg = (
                    "Couldn't get location from photo. "
                    "Please add the point on the map."
                )
                self._errors["location"] = self.error_class([msg])
        elif not c_data.get('location') and not exif:
            # User has not supplied location and there is no EXIF
            msg = "Please add a location for this sighting!"
            self._errors["location"] = self.error_class([msg])

        c_data['tree'] = None
        if c_data.get('tag_number'):
            try:
                c_data['tree'] = Tree.objects.get(
                    tag_number=c_data.get('tag_number'))
            except Tree.DoesNotExist:
                # Either this is mis-typed, or it is new.
                # for now, let's raise... I want a 'Claim a tree' page...
                # TODO: redirect to claim a tree or something... nicer.
                self._errors["tag_number"] = self.error_class(
                    ["This tag number hasn't been claimed yet! Go to 'Claim a tree'"])
        else:
            c_data['tree'] = Tree.objects.create(
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
