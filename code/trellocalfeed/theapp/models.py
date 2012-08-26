from django.db import models

class FeedUser(models.Model):
    user_name = models.CharField(max_length=1000)
    user_token = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    trello_member_id = models.CharField(max_length=100, unique=True)
    is_valid = models.BooleanField(default=True)
    
    last_access = models.BigIntegerField()
    created = models.BigIntegerField()

class Feed(models.Model):
    user_token = models.CharField(max_length=200)
    feed_user = models.ForeignKey(FeedUser)
    salt = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_valid = models.BooleanField(default=True)
    
    last_access = models.BigIntegerField()
    created = models.BigIntegerField()
    