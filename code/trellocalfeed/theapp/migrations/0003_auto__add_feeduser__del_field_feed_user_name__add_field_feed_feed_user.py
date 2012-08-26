# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedUser'
        db.create_table('theapp_feeduser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('trello_member_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_access', self.gf('django.db.models.fields.BigIntegerField')()),
            ('created', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('theapp', ['FeedUser'])

        # Deleting field 'Feed.user_name'
        db.delete_column('theapp_feed', 'user_name')

        # Adding field 'Feed.feed_user'
        db.add_column('theapp_feed', 'feed_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['theapp.FeedUser']),
                      keep_default=False)

        # Adding field 'Feed.is_valid'
        db.add_column('theapp_feed', 'is_valid',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'FeedUser'
        db.delete_table('theapp_feeduser')

        # Adding field 'Feed.user_name'
        db.add_column('theapp_feed', 'user_name',
                      self.gf('django.db.models.fields.CharField')(default='moo', max_length=1000),
                      keep_default=False)

        # Deleting field 'Feed.feed_user'
        db.delete_column('theapp_feed', 'feed_user_id')

        # Deleting field 'Feed.is_valid'
        db.delete_column('theapp_feed', 'is_valid')


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
            'trello_member_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['theapp']