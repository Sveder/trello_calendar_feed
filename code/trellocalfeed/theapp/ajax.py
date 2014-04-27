import json
import traceback

import django.core.mail as mail
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

import logic
import models
from views import _get_user_from_user_id

@dajaxice_register
def process_cards(request, token, username, userid, email):
    try:
        user = logic.get_or_create_user(token, username, userid, email)
        return simplejson.dumps({'user_url' : user.url,})
    except:
        return simplejson.dumps({'user_url' : "", "error" : traceback.format_exc()})
    
    
    
@dajaxice_register    
def create_feed(request, is_only_assigned, all_day_meeting, meeting_length, boards):
    try:
        if "cur_user" not in request.session:
            return simplejson.dumps({'feed_url' : "", "error" : "You need to be authorized to call this."})
        
        user = _get_user_from_user_id(request.session["cur_user"])
        feed_model = logic.create_feed(user, is_only_assigned, all_day_meeting, meeting_length, boards)
        return simplejson.dumps({'feed_url' : feed_model.url, 'feed_summary' : feed_model.summary, "feed_id" : feed_model.id})
    except:
        return simplejson.dumps({'feed_url' : "", "error" : traceback.format_exc()})
    
@dajaxice_register    
def delete_feed(request, feed_id):
    try:
        if "cur_user" not in request.session:
            return simplejson.dumps({'deleted' : False, "error" : "You need to be authorized to call this."})
        
        user = _get_user_from_user_id(request.session["cur_user"])
        try:
            feed_model = models.Feed.objects.get(id=feed_id, feed_user=user)
        except models.Feed.DoesNotExist:
            return simplejson.dumps({'deleted' : False, "error" : "You can't call this on an unexistant feed."})
        
        feed_model.is_valid = False
        feed_model.save()
        return simplejson.dumps({'deleted' : True, "feed_id" : feed_id})
    
    except:
        return simplejson.dumps({'deleted' : False, "error" : traceback.format_exc()})
    
@dajaxice_register    
def add_email(request, email):
    try:
        if "cur_user" not in request.session:
            return simplejson.dumps({"error" : "You need to be authorized to call this."})
        
        user = _get_user_from_user_id(request.session["cur_user"])
        user.email = email
        user.save()
        
        try:
            mail.send_mail("A new trello2ical user", "I got a new sign up:\n%s" % email,
                           "m@sveder.com", ["m@sveder.com"])
        except:
            print "an email was not sent buhuu"
            pass
        
        return simplejson.dumps({"error" : ""})
    except:
        return simplejson.dumps({"error" : traceback.format_exc()})