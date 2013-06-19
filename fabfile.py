#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import urllib

from django.core.files import File

from fabric.api import run, local, hosts, cd, task, env, get, abort
from fabric.contrib.console import confirm
from fabric.colors import red, green
from fabric.contrib import django


SETTINGS = 'local'


@task
def ias_ess():
    """Env for ias-ess"""
    env.hosts = ['ias-ess.org']
    env.user = 'stringfellow'


@task
def erase_all_local(settings=SETTINGS):
    """Nuke the Tree/Sighting objects."""
    django.settings_module('ashtag.settings.%s' % settings)
    from ashtag.apps.core.models import Sighting, Tree
    if confirm(red("Really delete all local Trees and Sightings?"), default=False):
        Tree.objects.all().delete()
        Sighting.objects.all().delete()
    else:
        abort("Not continuing with anything.")


@task
def get_sightings():
    """Get all un-synced sightings from IAS-ESS."""
    with cd('webapps/iasess/iasess/'):
        run('source ~/.virtualenvs/iasess/bin/activate')
        run('./manage.py dumpdata ias.Sighting --indent=4 --format=json > sightings_dump.json')
        get('sightings_dump.json', 'ias_ess_dump.json')


@task
def import_sightings(settings=SETTINGS, json_file='ias_ess_dump.json',
                     skip_images=False, pks__gte=0):
    """Put sightings from a fixture file into db.

    :param settings: change to change settings file inside ashtag.settings...
    :param json_file: change to use locally dumped json
    :param skip_images: set True to ignore images
    :param pks__gte: set > 0 to limit import (or do an update, etc.)

    """
    django.settings_module('ashtag.settings.%s' % settings)
    from ashtag.apps.core.models import Sighting, Tree
    dumped_json = ""
    with open(json_file, 'r') as fp:
        dumped_json = fp.read()
    sightings = json.loads(dumped_json)

    ash_sightings = filter(lambda x: x['fields']['taxon'] == 100004, sightings)
    not_rejects = filter(lambda x: not x['fields']['rejected'], ash_sightings)
    have_emails = filter(lambda x: x['fields']['email'], not_rejects)
    only_pks = sorted(
        filter(lambda x: x['pk'] >= int(pks__gte), have_emails),
        key=lambda x: x['pk'])

    print red("%s sightings don't have emails" % (
        len(not_rejects) - len(have_emails)
    ))

    unknown = Sighting.DISEASE_STATE.unknown
    diseased = Sighting.DISEASE_STATE.diseased
    print green("Processing %s sightings with PK >= %s" % (
        len(only_pks), pks__gte))
    for sighting in only_pks:
        fields = sighting['fields']
        tree = Tree.objects.create(
            location=fields['location'],
            creator_email=fields['email']
        )
        s = Sighting.objects.create(
            tree=tree,
            location=fields['location'],
            notes="Imported from IAS-ESS: http://ias-ess.org/ias/sighting/%s" % sighting['pk'],
            disease_state=diseased if fields['verified'] else unknown,
            created=fields['datetime'],
            creator_email=fields['email']
        )
        if not skip_images:
            image = urllib.urlretrieve(
                "http://ias-ess.org/static/media/%s" % fields['photo'])
            s.image.save(
                os.path.basename(fields['photo']),
                File(open(image[0]))
            )
        s.save()
    print green("Made %s Trees and Sightings, latest PK = %s" % (
        len(pks__gte), only_pks[-1]['pk']))
