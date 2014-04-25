import json

from django.test import TestCase
from django.test.client import RequestFactory

import theapp.ajax as ajax
import theapp.logic as logic
import theapp.models as models


EXCEPTION_STRING = "Exception from raise_exception."

def raise_exception(*args, **kargs):
    """
    Raise an exception.
    """
    raise Exception(EXCEPTION_STRING)


class TestProcessCards(TestCase):
    def test_proess_cards(self):
        """
        Test: User is retrieved.
        Expected result: No exceptions are raised
        """
        #Create a user for the test
        name = "moo"
        uid = "1234"
        token = "some token"
        email = "moo@lala.com"
        
        new_user = logic.get_or_create_user(token, name, uid, email)
        
        #Try and retreive it and see the info is the same:
        json_info = ajax.process_cards(None, token, name, uid, email)
        
        created_url = json.loads(json_info)["user_url"]
        
        retrieved_user = models.FeedUser.objects.get(url = created_url)
        
        self.assertEqual(retrieved_user.user_name , name, "User name is wrong.")
        self.assertEqual(retrieved_user.trello_member_id , uid, "User uid is wrong.")
        self.assertEqual(retrieved_user.user_token , token, "User token is wrong.")
        self.assertEqual(retrieved_user.email , email, "User email is wrong.")
        
        
    def test_exception_raised(self):
        """
        Test: An exception is raised creating the user.
        Expected result: Error message returned.
        """
        original_get_or_create_user = ajax.logic.get_or_create_user
        ajax.logic.get_or_create_user = raise_exception
        
        
        json_ret = ajax.process_cards(None, "token", "name", "uid", "email")
        json_ret = json.loads(json_ret)
        
        ajax.logic.get_or_create_user = original_get_or_create_user
        
        self.assertEqual(json_ret["user_url"], "", "User url returned when none were expected.")
        self.assertNotEqual(json_ret["error"], "", "Error not raised.")
        self.assertTrue(EXCEPTION_STRING in json_ret["error"], "Wrong exception returned")
        
        
class TestCreateFeed(TestCase):
    def setUp(self):
        self.user = logic.get_or_create_user("token", "user name", "1234", "email")
        self.factory = RequestFactory()
        
    def test_create_feed(self):
        """
        Test: User exists and everything goes ok.
        Expected result: No exceptions are raised
        """
        
        request = self.factory.get('/doesnt/matter')
        request.session = {"cur_user" : self.user.id}
        
        json_ret = json.loads(ajax.create_feed(request, True, True, 15, []))

        self.assertNotEqual(json_ret["feed_url"], "", "Url is empty.")
        self.assertNotEqual(json_ret["feed_summary"], "", "Summary is empty.")
        self.assertTrue("assigned only to me" in json_ret["feed_summary"], "Summary is wrong.")
        
    def test_no_user(self):
        """
        Test: No user in session.
        Expected result: Error returned.
        """
        request = self.factory.get('/doesnt/matter')
        request.session = {}
        
        json_ret = json.loads(ajax.create_feed(request, True, True, 15, []))

        self.assertEqual(json_ret["feed_url"], "", "Url not empty.")
        self.assertEqual(json_ret["error"], "You need to be authorized to call this.", "Wrong error returned.")
    
    def test_exception(self):
        """
        Test: logic.create_feed raises exception.
        Expected result: Error returned.
        """
        request = self.factory.get('/doesnt/matter')
        request.session = {"cur_user" : self.user.id}
        
        original_create_feed = ajax.logic.create_feed
        ajax.logic.create_feed = raise_exception
        
        json_ret = json.loads(ajax.create_feed(request, True, True, 15, []))
        ajax.logic.create_feed = original_create_feed

        self.assertEqual(json_ret["feed_url"], "", "Url not empty.")
        self.assertTrue(EXCEPTION_STRING in json_ret["error"], "Wrong error returned.")
        
        
class TestDeleteFeed(TestCase):
    def setUp(self):
        self.user = logic.get_or_create_user("token", "user name", "1234", "email")
        self.factory = RequestFactory()
        
    def test_delete_feed(self):
        """
        Test: User exists and feed exists.
        Expected result: No exceptions are raised
        """
        request = self.factory.get('/doesnt/matter')
        request.session = {"cur_user" : self.user.id}
        
        feed = logic.create_feed(self.user, True, True, 15, [])

        json_ret = json.loads(ajax.delete_feed(request, feed.id))
        feed = models.Feed.objects.get(id = feed.id)
        
        self.assertTrue(json_ret["deleted"], "Feed was not deleted")
        self.assertEqual(json_ret["feed_id"], feed.id, "Feed id is wrong.")
        self.assertFalse(feed.is_valid, "Feed was not marked as invalid.")

    def test_no_user(self):
        """
        Test: User doesn't exist in session.
        Expected result: Error will be returned.
        """
        request = self.factory.get('/doesnt/matter')
        request.session = {}
        
        feed = logic.create_feed(self.user, True, True, 15, [])

        json_ret = json.loads(ajax.delete_feed(request, feed.id))
        
        self.assertFalse(json_ret["deleted"], "Feed was deleted")
        self.assertEqual(json_ret["error"], "You need to be authorized to call this.", "Error is wrong.")
        self.assertTrue(feed.is_valid, "Feed was marked as invalid.")

    def test_no_feed(self):
        """
        Test: Feed doesn't exist.
        Expected result: Error will be returned.
        """
        request = self.factory.get('/doesnt/matter')
        request.session = {"cur_user" : self.user.id}
        
        json_ret = json.loads(ajax.delete_feed(request, -1))
        
        self.assertFalse(json_ret["deleted"], "Feed was deleted")
        self.assertEqual(json_ret["error"], "You can't call this on an unexistant feed.", "Error is wrong.")

    def test_exception(self):
        """
        Test: An exception is raised main code.
        Expected result: Error will be returned.
        """
        request = self.factory.get('/doesnt/matter')
        request.session = {"cur_user" : self.user.id}
        
        original_get_user_from_user_id = ajax._get_user_from_user_id
        ajax._get_user_from_user_id = raise_exception
        
        feed = logic.create_feed(self.user, True, True, 15, [])
        
        json_ret = json.loads(ajax.delete_feed(request, feed.id))
        ajax._get_user_from_user_id = original_get_user_from_user_id
        
        self.assertFalse(json_ret["deleted"], "Feed was deleted")
        self.assertTrue(EXCEPTION_STRING in json_ret["error"], "Error is wrong.")
        self.assertTrue(feed.is_valid, "Feed was deleted.")
