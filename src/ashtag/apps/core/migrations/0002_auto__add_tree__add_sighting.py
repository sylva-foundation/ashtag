# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tree'
        db.create_table(u'core_tree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Tree'])

        # Adding model 'Sighting'
        db.create_table(u'core_sighting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tree', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tree'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('disease_state', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Sighting'])


    def backwards(self, orm):
        # Deleting model 'Tree'
        db.delete_table(u'core_tree')

        # Deleting model 'Sighting'
        db.delete_table(u'core_sighting')


    models = {
        u'core.sighting': {
            'Meta': {'object_name': 'Sighting'},
            'disease_state': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tree']"})
        },
        u'core.tree': {
            'Meta': {'object_name': 'Tree'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']