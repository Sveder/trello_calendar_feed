import time
import random
import string
import hashlib
import datetime

import trello
import icalendar

import models

API_KEY = "9cf5a88e6a3a9897d59e55bfc327b5d5"

SALT_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()_+{}[]"
SALT_LENGTH = 16

def _create_salt_and_url(user_name):
    """
    Create a random salt and url hash from the given username. This is basically giving us some random long
    string - security 
    """
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

def get_or_create_user(token, username, userid):
    """
    Either get the user model that corresponds to the given user id or create a new user model.
    """
    now = time.time()
    try:
        user_model = models.FeedUser.objects.get(trello_member_id=userid)
    except models.FeedUser.DoesNotExist:
        salt, url = _create_salt_and_url(username)
        user_model = models.FeedUser(user_name=username, user_token=token, url=url, trello_member_id=userid, created=now)
    
    user_model.last_access = now
    user_model.save()
    
    return user_model
    
def create_calendar_from_feed(feed):
    """
    Create an ical object from the cards from the feed given.
    """
    client = trello.client.Trello(API_KEY, feed.user_token)
    boards = client.list_boards()
    
    card_list = []
    for board in boards:
        cards = board.list_cards("due,url")
        for card in cards:
            if card.due != None:
                card_start_time = card.due
                start_time = datetime.datetime.strptime(card_start_time, "%Y-%m-%dT%H:%M:%S.000Z")
                if start_time > datetime.datetime.now():
                    card_list.append(card)
                    
    return create_calendar_from_cards(card_list)
    
def get_all_board_names(token):
    """
    Get a list of all board names of the user whose token is given.
    """
    client = trello.client.Trello(API_KEY, token)
    boards = client.list_boards()
    board_names = []
    for board in boards:
        board.fetch()
        board_names.append(board.name)
    
    print board_names
    return board_names



def create_calendar_from_cards(card_list):
    """
    Create an ical object from the card list given and return it/
    """
    #Create calendar object:
    calendar = _create_calendar()
    
    #Create event for each card:
    for card in card_list:
        event = _create_event_from_card(card)
        calendar.add_component(event)
    
    return calendar
        
def _create_calendar():
    cal = icalendar.Calendar()
    cal.add("prodid", "-//sveder.com/trello_to_ical//EN")
    cal.add("version", "0.1")
    return cal

def _create_event_from_card(card):
    card_start_time = card.due
    start_time = datetime.datetime.strptime(card_start_time, "%Y-%m-%dT%H:%M:%S.000Z")
    end_time = start_time + datetime.timedelta(minutes=15)
    
    event = icalendar.Event()
    
    #hackity hack to maybe not add new line to summary:
    summary = card.name[:50] + "..."
    event.add("summary", "Trello Item: %s" % summary)
    event.add('DESCRIPTION', card.url)
    
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('dtstamp', start_time)
    event["uid"] = "%strello_to_ical" % card.id
    
    return event
    