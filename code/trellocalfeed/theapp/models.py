import traceback

from django.db import models

class FeedUser(models.Model):
    user_name = models.CharField(max_length=1000)
    user_token = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    trello_member_id = models.CharField(max_length=100, unique=True)
    is_valid = models.BooleanField(default=True)
    
    last_access = models.BigIntegerField()
    created = models.BigIntegerField()


class Board(models.Model):
    board_id = models.CharField(max_length=100, unique=True)
    name = models.TextField()
    

class Feed(models.Model):
    feed_user = models.ForeignKey(FeedUser)
    salt = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_valid = models.BooleanField(default=True)
    
    boards = models.ManyToManyField(Board)
    only_assigned = models.BooleanField(default=False)
    event_length = models.IntegerField(default=15)
    is_all_day_event = models.BooleanField(default=False)
    
    last_access = models.BigIntegerField()
    created = models.BigIntegerField()
    
    def get_relative_url(self):
        return "/feed/%s" % self.url
    
    relative_url = property(get_relative_url)
    
    def get_summary(self):
        try:
            summary = "A feed with cards "
            if self.only_assigned:
                summary += "assigned only to me, where events are "
            
            if self.is_all_day_event:
                summary += "all day "
            else:
                summary += "%s minutes " % self.event_length
            
            summary += ", from the following %s boards: " % len(self.boards.all())
            summary += ",".join([i.name for i in self.boards.all()])
            return summary
        except:
            print traceback.print_exc()

    summary = property(get_summary)
    
    
