# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Board', fields ['board_id']
        db.create_unique('theapp_board', ['board_id'])

        # Deleting field 'Feed.user_token'
        db.delete_column('theapp_feed', 'user_token')


    def backwards(self, orm):
        # Removing unique constraint on 'Board', fields ['board_id']
        db.delete_unique('theapp_board', ['board_id'])

        # Adding field 'Feed.user_token'
        db.add_column('theapp_feed', 'user_token',
                      self.gf('django.db.models.fields.CharField')(default='1', max_length=200),
                      keep_default=False)


    models = {
        'theapp.board': {
            'Meta': {'object_name': 'Board'},
            'board_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'theapp.feed': {
            'Meta': {'object_name': 'Feed'},
            'boards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['theapp.Board']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.BigIntegerField', [], {}),
            'event_length': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'feed_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['theapp.FeedUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_all_day_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_access': ('django.db.models.fields.BigIntegerField', [], {}),
            'only_assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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