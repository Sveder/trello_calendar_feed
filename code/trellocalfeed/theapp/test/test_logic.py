import json
import time

from django.test import TestCase
from django.conf import settings

import theapp.ajax as ajax
import theapp.logic as logic
import theapp.models as models
import theapp.trello as trello

from secrets import *

API_KEY = settings.TRELLO_API_KEY
EXCEPTION_STRING = "Exception from raise_exception."

def raise_exception(*args, **kargs):
    """
    Raise an exception.
    """
    raise Exception(EXCEPTION_STRING)


class TestCreateSaltAndURL(TestCase):
    def test_normal(self):
        """
        Test: Normal operation.
        Expected result: No exceptions are raised
        """
        username = "some username"
        salt, url = logic._create_salt_and_url(username)
        
        #Checking randomness is tricky without actually recreating the hashing function:
        self.assertNotEqual(salt, username)
        self.assertNotEqual(salt, url)
        self.assertNotEqual(url, username)
        
    
class TestGetOrCreateUser(TestCase):
    def test_model_exists(self):
        """
        Test: USer model exists.
        Expected result: Model will be returned.
        """
        username = "name"
        token = "token"
        url = "url"
        trello_member_id = "memberid"
        now = int(time.time())
        
        new_user = models.FeedUser(user_name=username, user_token=token, url=url, trello_member_id=trello_member_id, created=now, last_access=now)
        new_user.save()
                
        returned_user = logic.get_or_create_user(None, None, trello_member_id, "some email")
        
        self.assertEqual(returned_user.user_name, username)
        self.assertEqual(returned_user.user_token, token)
        self.assertEqual(returned_user.url, url)
        self.assertEqual(returned_user.created, now)
        
    
    def test_new_model(self):
        """
        Test: USer model doesn't exists.
        Expected result: New model will be created and returned.
        """
        username = "name"
        token = "token"
        email="email"
        trello_member_id = "non existent"
        
        try:
            models.FeedUser.objects.get(trello_member_id=trello_member_id)
            raise Exception("A user with the trello member id %s already exists." % trello_member_id)
        except models.FeedUser.DoesNotExist:
            pass
        
        new_user = logic.get_or_create_user(token, username, trello_member_id, email)
        
        self.assertEqual(new_user.user_name, username)
        self.assertEqual(new_user.user_token, token)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.is_valid)
        
        
class TestCreateCalendarFromFeed(TestCase):
    def setUp(self):
        self.user = logic.get_or_create_user(USER_TOKEN, "some name", USER_ID, "moo@lala.com")
        
    def test_subset_of_boards(self):
        """
        Test: Create a calendar from a subset of the boards the user has.
        Expected result: Only the requested boards will be in calendar.
        """
        #Create a feed with only one of the boards:
        feed = logic.create_feed(self.user, False, False, 15, TEST_BOARDS[:1])
        cal = logic.create_calendar_from_feed(feed)
        
        #check that there are entries from test board 1 but not test board 2:
        self.assertEqual(len(cal.subcomponents), 2, "More cards then expected.")
        for comp in cal.subcomponents:
            self.assertTrue(comp["SUMMARY"].startswith("tb1"), "Wrong test board cards added.")
            self.assertFalse("nd" in comp["SUMMARY"], "No due date card was added.")
    
    def test_unassigned_not_added(self):
        """
        Test: Test that the unsassigned flag in the feed is respected.
        Expected result: Only the assigned cards in bot boards will be in the feed.
        """
        #Create a feed with only assigned cards:
        feed = logic.create_feed(self.user, True, False, 15, TEST_BOARDS)
        cal = logic.create_calendar_from_feed(feed)
        
        #check that there are entries from both boards, but only assigned ones:
        self.assertEqual(len(cal.subcomponents), 2, "More cards then expected.")
        for comp in cal.subcomponents:
            self.assertFalse("na" in comp["SUMMARY"], "Not assigned card added to cal.")
    
    def test_unassigned_not_added(self):
        """
        Test: Test that the unsassigned flag in the feed is respected.
        Expected result: Only the assigned cards in bot boards will be in the feed.
        """
        #Create a feed with only assigned cards:
        feed = logic.create_feed(self.user, True, False, 15, TEST_BOARDS)
        cal = logic.create_calendar_from_feed(feed)
        
        #check that there are entries from both boards, but only assigned ones:
        self.assertEqual(len(cal.subcomponents), 2, "More cards then expected.")
        for comp in cal.subcomponents:
            self.assertFalse("na" in comp["SUMMARY"], "Not assigned card added to cal.")
            self.assertFalse("nd" in comp["SUMMARY"], "No due date card was added.")

        
class TestCreateFeed(TestCase):
    def setUp(self):
        self.user = logic.get_or_create_user(USER_TOKEN, "some name", USER_ID, "moo@lala.com")
        
    def test_no_boards(self):
        """
        Test: Call create_feed without boards.
        Expected result: Feed will be created without any boards.
        """
        #Create a feed with only one of the boards:
        feed = logic.create_feed(self.user, False, False, 15, [])
        self.assertEqual(len(feed.boards.all()), 0)
        
    def test_with_boards_not_in_db(self):
        """
        Test: Call create_feed with boards not in the db.
        Expected result: A feed with boards will be returned and board will be created in db.
        """
        try:
            models.Board.objects.get(board_id=TEST_BOARDS[0])
            self.fail("A board was already in the db.")
        except models.Board.DoesNotExist:
            pass
        
        feed = logic.create_feed(self.user, False, False, 15, TEST_BOARDS[:1])
        
        self.assertEqual(len(feed.boards.all()), 1, "Wrong number of boards returned")
        self.assertFalse(feed.only_assigned)
        self.assertFalse(feed.is_all_day_event)
        self.assertEqual(feed.event_length, 15)
        
        models.Board.objects.get(board_id=TEST_BOARDS[0])
    
    def test_with_boards_in_db(self):
        """
        Test: Call create_feed with boards that are already in db.
        Expected result: A feed with boards will be returned.
        """
        #Create a feed with only one of the boards:
        models.Board(board_id=TEST_BOARDS[1], name="some name").save()
        
        feed = logic.create_feed(self.user, False, False, 15, TEST_BOARDS[1:])
        
        self.assertEqual(len(feed.boards.all()), 1, "Wrong number of boards returned")
        self.assertFalse(feed.only_assigned)
        self.assertFalse(feed.is_all_day_event)
        self.assertEqual(feed.event_length, 15)
        

class TestCreateCalendarFromCards(TestCase):
    def setUp(self):
        self.user = logic.get_or_create_user(USER_TOKEN, "some name", USER_ID, "moo@lala.com")
        self.feed = logic.create_feed(self.user, False, False, 15, TEST_BOARDS)
        
    def test_no_cards(self):
        """
        Test: Call create_calendar_from_cards with empty card list.
        Expected result: Empty calendar will be created.
        """
        #Create a feed with only one of the boards:
        cal = logic.create_calendar_from_cards([], self.feed)
        
        self.assertEqual(cal.subcomponents, [])
    
    def test_with_cards(self):
        """
        Test: Call create_calendar_from_cards with cards.
        Expected result: Calendar with subcomponents will be created.
        """
        #Create a feed with only one of the boards:
        client = trello.client.Trello(API_KEY, self.user.user_token)
        boards = client.list_boards()
        
        test_boards = [board for board in boards if board.id in TEST_BOARDS]
        card_list = []
        for b in test_boards:
            card_list += b.list_cards()
        
        card_list = [c for c in card_list if c.due]
    
        cal = logic.create_calendar_from_cards(card_list, self.feed)
        
        self.assertEqual(len(cal.subcomponents), 4)
        
    
class TestCreateCalendar(TestCase):
    def test_create_calendar(self):
        """
        Test: Call _create_calendar.
        Expected result: An empty calendar will be returned.
        """
        cal = logic._create_calendar()
        
        self.assertEqual(cal.subcomponents, [])
        

class TestGetCategoriesFromLabels(TestCase):
    def test_without_labels(self):
        """
        Test: Call _get_categories_from_labels with a card with no labels.
        Expected result: No categories will be returned.
        """
        #Mock a card object:
        class MockCard:
            json_obj = {"labels" : []}
            
        categories = logic._get_categories_from_labels(MockCard())
        self.assertEqual(categories, [])
    
    def test_without_labels(self):
        """
        Test: Call _get_categories_from_labels with a card with labels.
        Expected result: Categories will be returned both based on color and name.
        """
        #Mock a card and label object:
        name = "a name"
        color = "a color"
        class MockCard:
            json_obj = {"labels" : [{"name" : name}, {"color" : color}]}
            
        categories = logic._get_categories_from_labels(MockCard())
        self.assertTrue(name in categories)
        self.assertTrue(color in categories)
        

