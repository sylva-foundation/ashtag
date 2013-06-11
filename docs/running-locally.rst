Running Locally
===============

Requirements
------------

AshTag uses GeoDjango for storing locations. See the `GeoDjango installation instructions`_.

However, users of brew on Mac OS X may find the following useful:
    
    sudo pip install numpy
    brew update
    brew install geos proj postgis gdal libgeoip

.. _GeoDjango installation instructions: https://docs.djangoproject.com/en/1.5/ref/contrib/gis/install/