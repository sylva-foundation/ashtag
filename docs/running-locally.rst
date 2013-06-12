Running Locally
===============

Using Vagrant / VirtualBox (simple)
-----------------------------------

AshTag is packaged as a `Vagrant`_ project, which allows you to get up and running 
quickly using a virtual machine. You will need to download and install the following:

- `VirtualBox`_
- `Vagrant`_

Clone the AshTag repository into a directory of your choosing::

    git clone https://github.com/adapt/ashtag.git
    cd ashtag

Now setup the VM using vagrant::

    vagrant up

Once complete, you can SSH into the sever and run the django development server::

    vagrant ssh
    # You are now on the virtual machine
    django-admin.py runserver

The files in your cloned repository will be kept in sync with those on the VM, so you 
can go ahead and start editing files locally.

Using virtualenvwrapper on Mac OS X (more involved)
---------------------------------------------------

AshTag uses GeoDjango for storing locations. See the `GeoDjango installation instructions`_.

However, users of brew on Mac OS X may find the following useful::
    
    sudo pip install numpy
    brew update
    brew install geos proj postgis gdal libgeoip

.. _GeoDjango installation instructions: https://docs.djangoproject.com/en/1.5/ref/contrib/gis/install/
.. _Vagrant: http://www.vagrantup.com/
.. _VirtualBox: https://www.virtualbox.org/