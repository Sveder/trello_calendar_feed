from django.db import models

class Feed(models.Model):
    user_token = models.CharField(max_length=200)
    user_name = models.CharField(max_length=1000)
    
    salt = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    last_access = models.BigIntegerField()
    created = models.BigIntegerField()
    

