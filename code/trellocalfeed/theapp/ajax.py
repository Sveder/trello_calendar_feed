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
    
    
    
    
    
    
    