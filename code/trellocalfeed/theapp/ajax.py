import json

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

import logic

@dajaxice_register
def process_cards(request, token, username):
    try:
        feed = logic.get_or_create_feed_in_db(token, username)
        return simplejson.dumps({'url' : feed.url})
    except:
        import traceback
        return simplejson.dumps({'url' : "", "error" : traceback.format_exc()})
