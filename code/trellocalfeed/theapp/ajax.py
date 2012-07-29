import json

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

import logic

@dajaxice_register
def process_cards(request, cards_json, token, username):
    print cards_json
    print token
    print username
    
    
    
    try:
        feed = logic.get_or_create_feed_in_db(token, username)
        print feed, feed.user_name, feed.user_token, feed.url, feed.salt
        cards = json.loads(cards_json)
        calendar = logic.create_calendar_from_cards(cards)
    except:
        import traceback
        traceback.print_exc()
    
    return simplejson.dumps({'message':'Hello World'})
