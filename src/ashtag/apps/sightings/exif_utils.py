#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


def _convert_to_degress(value):
    """Convert the GPS coordinates stored in EXIF to degress in float format"""
    values = value.values

    d0 = values[0].num
    d1 = values[0].den
    d = float(d0) / float(d1)

    m0 = values[1].num
    m1 = values[1].den
    m = float(m0) / float(m1)

    s0 = values[2].num
    s1 = values[2].den
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif):
    """Return lat,long if available from exif_data."""
    lat = None
    lon = None

    if len(filter(lambda k: str(k).startswith('GPS'), exif.keys())):
        gps_latitude = exif.get("GPS GPSLatitude", None)
        gps_latitude_ref = exif.get("GPS GPSLatitudeRef", None)
        gps_longitude = exif.get("GPS GPSLongitude", None)
        gps_longitude_ref = exif.get("GPS GPSLongitudeRef", None)

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref.values != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref.values != "E":
                lon = 0 - lon

    return lat, lon
