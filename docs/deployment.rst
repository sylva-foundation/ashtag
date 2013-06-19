Deployment
==========

To deploy to dotCloud, follow the instructions here:
http://docs.dotcloud.com/firststeps/install/ (though, as we are using
virtualenv, you won't need to install pip or use `sudo` as you'll be
doing this inside the virtualenv.) You'll need to get the credentials
for dotcloud from the maintainers of ashtag.

Once you have done that, add the following to your
`$VIRTUAL_ENV/bin/postactivate` hook:

.. code-block:: bash
    
    dotcloud connect --git --branch master ashtag


Now, run the following:

.. code-block:: bash
    
    dotcloud push


That's it!
