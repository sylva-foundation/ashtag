Running Locally
===============

Using Vagrant / VirtualBox (simple)
-----------------------------------

AshTag is packaged as a `Vagrant`_ project, which allows you to get up and running 
quickly using a virtual machine. You will need to download and install the following:

- `VirtualBox`_
- `Vagrant`_

Clone the AshTag repository into a directory of your choosing:
    
.. code-block:: bash

    # Note use "git://github.com/adapt/ashtag.git" for read-only access
    git clone git@github.com:adapt/ashtag.git
    cd ashtag

Now setup the VM using vagrant:
    
.. code-block:: bash

    # Start the VM. As the VM doesn't exist, this will download and 
    # configure it
    vagrant up

Once complete, you can SSH into the sever and run the django development server:

.. code-block:: bash

    # SSH into the VM
    vagrant ssh
    # You are now on the virtual machine, so you can run the django dev server
    runserver

You should now be able to open http://127.0.0.1:8080/ in your web browser.

The files in your cloned repository will be kept in sync with those on the VM, so you 
can go ahead and start editing files locally.

.. note:: 

    ``runserver`` is simply and alias for the somewhat longer command::

        django-admin.py runserver 0.0.0.0:8080


Starting and Stopping the Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are finished working on the project, you can shut down the virtual machine to 
save on system resources:

.. code-block:: bash

    # Shut down the VM
    vagrant halt 

When you come back to the project, you can simply start it using:

.. code-block:: bash

    # Start the VM again (as the VM exists, this will be a relatively fast)
    vagrant up

Reconfiguring the Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the Vagrant config or build scripts change it will probably be necessary to 
rebuild the VM. To do this, simply destroy and recreate it:

.. code-block:: bash

    vagrant destroy
    vagrant up

Using virtualenvwrapper on Mac OS X (more involved)
---------------------------------------------------

AshTag uses GeoDjango for storing locations. See the `GeoDjango installation instructions`_.

However, users of brew on Mac OS X may find the following useful:

.. code-block:: bash
    
    sudo pip install numpy
    brew update
    brew install geos proj postgis gdal libgeoip

.. _GeoDjango installation instructions: https://docs.djangoproject.com/en/1.5/ref/contrib/gis/install/
.. _Vagrant: http://www.vagrantup.com/
.. _VirtualBox: https://www.virtualbox.org/