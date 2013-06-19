# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sighting.flagged'
        db.add_column(u'core_sighting', 'flagged',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Sighting.hidden'
        db.add_column(u'core_sighting', 'hidden',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sighting.flagged'
        db.delete_column(u'core_sighting', 'flagged')

        # Deleting field 'Sighting.hidden'
        db.delete_column(u'core_sighting', 'hidden')


    models = {
        u'core.sighting': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Sighting'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'creator_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'disease_state': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'jjiadr'", 'max_length': '6', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tree']"})
        },
        u'core.tree': {
            'Meta': {'ordering': "('tag_number',)", 'object_name': 'Tree'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'creator_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'exemplar': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exemplary_of'", 'null': 'True', 'to': u"orm['core.Sighting']"}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'kpnc2r'", 'max_length': '6', 'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'tag_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']