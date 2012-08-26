# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FeedUser.user_token'
        db.add_column('theapp_feeduser', 'user_token',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=200),
                      keep_default=False)

        # Adding unique constraint on 'FeedUser', fields ['trello_member_id']
        db.create_unique('theapp_feeduser', ['trello_member_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'FeedUser', fields ['trello_member_id']
        db.delete_unique('theapp_feeduser', ['trello_member_id'])

        # Deleting field 'FeedUser.user_token'
        db.delete_column('theapp_feeduser', 'user_token')


    models = {
        'theapp.feed': {
            'Meta': {'object_name': 'Feed'},
            'created': ('django.db.models.fields.BigIntegerField', [], {}),
            'feed_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.FeedUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_access': ('django.db.models.fields.BigIntegerField', [], {}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_token': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'theapp.feeduser': {
            'Meta': {'object_name': 'FeedUser'},
            'created': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_access': ('django.db.models.fields.BigIntegerField', [], {}),
            'trello_member_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user_token': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['theapp']