import json

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

import logic

@dajaxice_register
def process_cards(request, token, username):
    try:
        feed = logic.get_or_create_feed_in_db(token, username)
        calendar = logic.create_calendar_from_feed(feed)
        ical_feed = calendar.to_ical()
        return simplejson.dumps({'ical' : ical_feed, "url" : feed.url})
    except:
        import traceback
        return simplejson.dumps({'ical' : "", "error" : traceback.format_exc()})
