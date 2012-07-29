import time
import random
import string
import hashlib
import icalendar

import models

SALT_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()_+{}[]"
SALT_LENGTH = 16

def _create_salt_and_url(user_name):
    salt = "".join([random.choice(SALT_ALPHABET) for i in xrange(SALT_LENGTH)])
    url = hashlib.sha512(user_name + salt).hexdigest()
    
    return salt, url

def get_or_create_feed_in_db(token, user_name):
    """
    Either get the feed model for the user_name given or create it if it doesn't exist.
    """
    now = time.time()
    try:
        feed_model = models.Feed.objects.get(user_name=user_name, user_token=token)
    except models.Feed.DoesNotExist:
        try:
            feed_model = models.Feed.objects.get(user_name=user_name)
            feed_model.token = token
        except models.Feed.DoesNotExist:
            salt, url = _create_salt_and_url(user_name)
            feed_model = models.Feed(user_token=token, user_name=user_name, created=now, last_access=now, url=url, salt=salt)
    
    feed_model.last_access = now
    feed_model.save()
    
    return feed_model
            
    
        
    

def create_calendar_from_cards(card_list):
    """
    Create an ical string from the card list given and return
    """
    #Create calendar object:
    calendar = _create_calendar()
    
    #Create event for each card:
    for card in card_list:
        event = _create_event_from_card(card)
        calendar.add_component(event)
        
    

def _create_calendar():
    cal = icalendar.Calendar()
    cal.add("prodid", "-//sveder.com/trello_to_ical//EN")
    cal.add("version", "0.1")
    return cal

def _create_event_from_card(card):
    card_start_time = card["due"]
    print card_start_time
    
    event = icalendar.Event()
    event.add("summary", "Trello Item: %s" % card["name"])
    
    
    #event["uid"] = "%s.%s@trello_to_ical" % (card)