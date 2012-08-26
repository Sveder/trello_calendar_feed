# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('theapp_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_access', self.gf('django.db.models.fields.BigIntegerField')()),
            ('created', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('theapp', ['Feed'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('theapp_feed')


    models = {
        'theapp.feed': {
            'Meta': {'object_name': 'Feed'},
            'created': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.BigIntegerField', [], {}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user_token': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['theapp']