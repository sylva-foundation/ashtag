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

This section of the guide assumes you already have ``virtualenvwrapper`` setup. 
Checkout the `virtualenvwrapper documentation`_ for details of how to do this.

First, you will need to checkout the code:

.. code-block:: bash

    # Note use "git://github.com/adapt/ashtag.git" for read-only access
    git clone git@github.com:adapt/ashtag.git
    cd ashtag

Setting up the Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the dependencies for the local development environment (note you have
to install django first, because django-registration has a bug):

.. code-block:: bash

    pip install Django==1.5.1
    pip install -r requirements/localdev.txt


Now edit your environment's ``postactivate`` hook to include the following:

.. code-block:: bash
    
    # Add this to your postactive hook ($VIRTUAL_ENV/bin/postactivate)
    export PYTHONPATH="$PROJECT_HOME/ashtag/src:$PROJECT_HOME/ashtag/lib"
    export DJANGO_SETTINGS_MODULE=ashtag.settings.localdev
    export DJANGO_SECRET_KEY="RANDOM STRING HERE"

.. warning::
    
    Ensure you replace `RANDOM STRING HERE` with a random string, especially for deployment.

And now souce the file to load the new settings into your environment:

.. code-block:: bash

    source $VIRTUAL_ENV/bin/postactivate

Setup Postgres / PostGIS
------------------------

For those on Mac OS X, we recommend using `Postgres.app`_. In order to
enable the spatial element, simply create a database (let's call it ashtag) and
then enable the spatial element:

.. code-block:: bash

    createdb ashtag
    psql -h localhost ashtag

    ashtag=# CREATE EXTENSION postgis;

In theory, that's it...

Note that we do ``-h localhost`` because the Postgres.app is not using the normal
sockets approach, rather it binds to 0.0.0.0 (or 127.0.0.1 by default I think)
on port 5432. If you're using linux then probably you don't need that bit.

Setup GeoDjango
~~~~~~~~~~~~~~~

AshTag uses GeoDjango for storing locations. See the `GeoDjango installation instructions`_.

However, users of brew on Mac OS X may find the following useful:

.. code-block:: bash
    
    sudo pip install numpy
    brew update
    brew install geos proj postgis gdal libgeoip




Start it up
~~~~~~~~~~~

Now sync the db and start the development server:

.. code-block:: bash
    
    django-admin.py syncdb
    django-admin.py migrate
    django-admin.py runserver

.. _GeoDjango installation instructions: https://docs.djangoproject.com/en/1.5/ref/contrib/gis/install/
.. _Vagrant: http://www.vagrantup.com/
.. _VirtualBox: https://www.virtualbox.org/
.. _virtualenvwrapper documentation: http://virtualenvwrapper.readthedocs.org/
.. _Postgress.app: http://postgresapp.com/

