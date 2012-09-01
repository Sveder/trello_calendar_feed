# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Board'
        db.create_table('theapp_board', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('theapp', ['Board'])

        # Adding field 'Feed.only_assigned'
        db.add_column('theapp_feed', 'only_assigned',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Feed.event_length'
        db.add_column('theapp_feed', 'event_length',
                      self.gf('django.db.models.fields.IntegerField')(default=15),
                      keep_default=False)

        # Adding field 'Feed.is_all_day_event'
        db.add_column('theapp_feed', 'is_all_day_event',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field boards on 'Feed'
        db.create_table('theapp_feed_boards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm['theapp.feed'], null=False)),
            ('board', models.ForeignKey(orm['theapp.board'], null=False))
        ))
        db.create_unique('theapp_feed_boards', ['feed_id', 'board_id'])


    def backwards(self, orm):
        # Deleting model 'Board'
        db.delete_table('theapp_board')

        # Deleting field 'Feed.only_assigned'
        db.delete_column('theapp_feed', 'only_assigned')

        # Deleting field 'Feed.event_length'
        db.delete_column('theapp_feed', 'event_length')

        # Deleting field 'Feed.is_all_day_event'
        db.delete_column('theapp_feed', 'is_all_day_event')

        # Removing M2M table for field boards on 'Feed'
        db.delete_table('theapp_feed_boards')


    models = {
        'theapp.board': {
            'Meta': {'object_name': 'Board'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
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