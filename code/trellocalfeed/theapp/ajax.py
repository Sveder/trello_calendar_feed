import json
import traceback

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

import logic

@dajaxice_register
def process_cards(request, token, username, userid):
    try:
        user = logic.get_or_create_user(token, username, userid)
        return simplejson.dumps({'user_url' : user.url,})
    except:
        return simplejson.dumps({'user_url' : "", "error" : traceback.format_exc()})
    
    
    
@dajaxice_register    
def create_feed(request, is_only_assigned, all_day_meeting, meeting_length, boards):
    try:
        print is_only_assigned
        print all_day_meeting
        print meeting_length
        print boards
        if "cur_user" not in request.session:
            return simplejson.dumps({'feed_url' : "", "error" : "You need to be authorized to call this."})
        
        user = request.session["cur_user"]
        feed_model = logic.create_feed(user, is_only_assigned, all_day_meeting, meeting_length, boards)
        return simplejson.dumps({'feed_url' : feed_model.url,})
    except:
        return simplejson.dumps({'feed_url' : "", "error" : traceback.format_exc()})