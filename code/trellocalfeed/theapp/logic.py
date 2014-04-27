import json
import time
import random
import string
import hashlib
import datetime

import pytz
import trello
import icalendar
from django.conf import settings

API_KEY = settings.TRELLO_API_KEY


import models


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

def get_or_create_user(token, username, userid, email):
    """
    Either get the user model that corresponds to the given user id or create a new user model.
    """
    now = time.time()
    try:
        user_model = models.FeedUser.objects.get(trello_member_id=userid)
    except models.FeedUser.DoesNotExist:
        salt, url = _create_salt_and_url(username)
        user_model = models.FeedUser(user_name=username, user_token=token, url=url, trello_member_id=userid, created=now)
    
    email = email.strip()
    if email:
        user_model.email = email
        
    user_model.last_access = now
    user_model.save()
    
    return user_model
    
def create_calendar_from_feed(feed):
    """
    Create an ical object from the cards from the feed given.
    """
    client = trello.client.Trello(API_KEY, feed.feed_user.user_token)
    
    card_list = []    
    
    boards = client.list_boards()
    board_ids = feed.boards.all().values_list("board_id")
    board_ids = [i[0] for i in board_ids]
    
    for board in boards:
        if board.id not in board_ids:
            continue
        
        cards = board.list_cards()
        for card in cards:
            if (feed.only_assigned) and (feed.feed_user.trello_member_id not in card.assignees):
                continue            
            
            if card.due != None:
                card_list.append(card)
                    
    return create_calendar_from_cards(card_list, feed)
    

def get_all_boards(token):
    client = trello.client.Trello(API_KEY, token)
    boards = client.list_boards()
    
    for board in boards:
        board.fetch()
    
    return boards


def create_feed(user, is_only_assigned, all_day_meeting, meeting_length, boards):
    salt, url = _create_salt_and_url(user.user_name)

    now = time.time()
    feed_model = models.Feed(feed_user=user, salt=salt, url=url, only_assigned=is_only_assigned,
                             is_all_day_event=all_day_meeting, event_length=meeting_length,
                             last_access=now, created=now)
    
    feed_model.save()
    
    client = trello.client.Trello(API_KEY, user.user_token)
    for board in boards:
        board_id = board.replace("checkbox_board_", "")
        try:
            board_model = models.Board.objects.get(board_id=board_id, )
        except models.Board.DoesNotExist:
            board_from_trello = trello.client.Board(client, board_id)
            board_from_trello.fetch()
            board_name = board_from_trello.name
            
            board_model = models.Board(board_id=board_id, name=board_name)
            board_model.save()
            
        feed_model.boards.add(board_model)
    
    return feed_model
    


def create_calendar_from_cards(card_list, feed):
    """
    Create an ical object from the card list given and return it/
    """
    #Create calendar object:
    calendar = _create_calendar()
    
    #Create event for each card:
    for card in card_list:
        event = _create_event_from_card(card, feed)
        calendar.add_component(event)
    
    return calendar
        
def _create_calendar():
    cal = icalendar.Calendar()
    cal.add("prodid", "-//sveder.com/trello_to_ical//EN")
    cal.add("version", "2.0")
    return cal

def _get_categories_from_labels(card):
    card_date = card.json_obj
    labels = card_date["labels"]
    categories = []
    for label in labels:
        label_name = label["name"] if label["name"] else label["color"]
        categories.append(label_name)
        
    return categories

def _create_event_from_card(card, feed):
    card_start_time = card.due
    start_time_struct = time.strptime(card_start_time, "%Y-%m-%dT%H:%M:%S.000Z")
    start_time = datetime.datetime(*(start_time_struct[:6]), tzinfo=pytz.utc)
    
    if feed.is_all_day_event:
        start_time = datetime.date(start_time.year, start_time.month, start_time.day)
        end_time = start_time + datetime.timedelta(days=1)
    else:
        end_time = start_time + datetime.timedelta(minutes=feed.event_length)
    
    event_description = u"\n---\nCard URL -\n%s" % card.url
    if card.description:
        event_description = u"%s\n%s" % (card.description, event_description)
        
    event_summary = card.name
    event_location = card.board.name
    
    categories = _get_categories_from_labels(card)
    categories = ",".join(categories)
    
    event = icalendar.Event()
    
    event.add("SUMMARY", event_summary)
    event.add("DESCRIPTION", event_description)
    event.add("CATEGORIES", categories)
    
    event.add("URL", card.url)
    event.add("LOCATION", event_location)
    
    event.add("DTSTART", start_time)
    event.add("DTEND", end_time)
    
    #Add some specific headers for full day events:
    if feed.is_all_day_event:
        event.add("X-FUNAMBOL-ALLDAY", "TRUE")
        event.add("X-MICROSOFT-CDO-ALLDAYEVENT", "TRUE") 
        
    now_struct = time.gmtime()
    stamp_time = datetime.datetime(*now_struct[:6])
    event.add("DTSTAMP", stamp_time)
    
    event["uid"] = "%strello_to_ical" % card.id
    
    return event
    