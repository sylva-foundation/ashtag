#!/usr/bin/env python
# -*- coding: utf-8 -*-
from decimal import Decimal

import floppyforms as flforms

from exifpy import EXIF

from .models import Sighting
from .exif_utils import get_lat_lon


class PointWidget(flforms.gis.PointWidget, flforms.gis.BaseOsmWidget):
    pass


class SightingForm(flforms.ModelForm):

    location = flforms.gis.PointField(required=False, widget=PointWidget)

    class Meta:
        model = Sighting

        widgets = {
            'location': PointWidget,
        }

    def clean(self):
        """Do some work to get EXIF, locations etc."""
        c_data = self.cleaned_data
        exif = None
        try:
            f = c_data['photo'].file
            f.seek(0)
            exif = EXIF.process_file(f)
            # weird little hack for some vals are malformatted...
            for i in exif.items():
                try:
                    str(i)
                except:
                    exif[i[0]] = i[1].printable
        except Exception, e:
            import logging
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

        return c_data
