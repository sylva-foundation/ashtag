#!/bin/bash -e

# Script to set up a Django project on Vagrant.

# Installation settings

PROJECT_NAME=ashtag

DB_NAME=$PROJECT_NAME
VIRTUALENV_NAME=$PROJECT_NAME

PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
PIP_DOWNLOAD_CACHE=$PROJECT_DIR/.pip_download_cache

PGSQL_VERSION=9.1

cp -p $PROJECT_DIR/vagrant/install/etc-bash.bashrc /etc/bash.bashrc

# Need to fix locale so that Postgres creates databases in UTF-8
if [ ! -f /etc/vagrant-locale-gen-flag ]; then
    locale-gen en_GB.UTF-8
    dpkg-reconfigure locales
    touch /etc/vagrant-locale-gen-flag
fi

export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8

# Post-gis repositories
apt-get install -y python-software-properties
apt-add-repository -y ppa:sharpie/for-science
apt-add-repository -y ppa:sharpie/postgis-stable
apt-add-repository -y ppa:ubuntugis/ubuntugis-unstable
apt-add-repository -y ppa:olivier-berten/geo

# Install essential packages from Apt
apt-get update -y
# Python dev packages
apt-get install -y build-essential python python-dev python-setuptools python-pip
# Dependencies for image processing with PIL
apt-get install -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev
# Other required utilities
apt-get install -y git

# Postgres + PostGIS
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' libgdal-dev|grep "install ok installed"|true)
if [ "" == "$PKG_OK" ]; then
    apt-get install -y binutils libproj-dev build-essential postgresql-9.1 postgresql-server-dev-9.1 libxml2-dev proj libjson0-dev xsltproc docbook-xsl docbook-mathml gettext postgresql-contrib-9.1 pgadmin3
    apt-get install -y libgdal-dev
fi


# postgresql global setup
cp $PROJECT_DIR/vagrant/install/pg_hba.conf /etc/postgresql/$PGSQL_VERSION/main/
/etc/init.d/postgresql reload

# postgis setup
apt-get install -y postgresql-9.1-postgis2 

# postgres user & db setup
psql postgres postgres -c 'CREATE ROLE vagrant WITH SUPERUSER LOGIN' || true
psql postgres vagrant -c 'CREATE DATABASE ashtag' || true
psql ashtag vagrant -c 'CREATE EXTENSION postgis' || true

# virtualenv global setup
easy_install -U pip
easy_install virtualenv virtualenvwrapper stevedore virtualenv-clone

# bash environment global setup
ln -sf $PROJECT_DIR/vagrant/install/bashrc /home/vagrant/.bashrc
ln -sf $PROJECT_DIR/vagrant/install/profile /home/vagrant/.profile
ln -sf $PROJECT_DIR/vagrant/install/motd /home/vagrant/.motd
su - vagrant -c "mkdir -p $PIP_DOWNLOAD_CACHE"

# ---

# postgresql setup for project (ignore any error if it already exists)
createdb -Upostgres $DB_NAME || true

# virtualenv setup for project
if [ ! -d $VIRTUALENV_DIR ]; then
    # Note that we install django here as is needed during the install of django-registration
    su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR && \
        echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
        $VIRTUALENV_DIR/bin/pip install django==1.5
        "
fi

su - vagrant -c "$VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements/localdev.txt"

# Django project setup
su - vagrant -c "django-admin.py syncdb --noinput && django-admin.py migrate"


cat << EOF

======================================================================

AshTag virtual machine setup complete. Now SSH into your new VM using:

    vagrant ssh
    
Then run the django development server with:

    runserver
    
Then access AshTag in your web browser here:

    http://127.0.0.1:8080

EOF