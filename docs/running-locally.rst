Running Locally
===============

Using Vagrant / VirtualBox (simple)
-----------------------------------

AshTag is packaged as a `Vagrant`_ project, which allows you to get up and running 
quickly using a virtual machine. You will need to download and install the following:

- `VirtualBox`_
- `Vagrant`_

Clone the AshTag repository into a directory of your choosing::
    
    # Note use "git://github.com/adapt/ashtag.git" for read-only access
    git clone git@github.com:adapt/ashtag.git
    cd ashtag

Now setup the VM using vagrant::
    
    # Start the VM. As the VM doesn't exist, this will download and 
    # configure it
    vagrant up

Once complete, you can SSH into the sever and run the django development server::
    
    # SSH into the VM
    vagrant ssh
    # You are now on the virtual machine, so you can run the django dev server
    django-admin.py runserver

The files in your cloned repository will be kept in sync with those on the VM, so you 
can go ahead and start editing files locally.

Starting and Stopping the Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are finished working on the project, you can shut down the virtual machine to 
save on system resources::

    # Shut down the VM
    vagrant halt 

When you come back to the project, you can simply start it using::

    # Start the VM again (as the VM exists, this will be a relatively fast)
    vagrant up


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