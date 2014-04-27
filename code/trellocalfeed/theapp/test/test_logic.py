import json
import time

from django.test import TestCase

import theapp.ajax as ajax
import theapp.logic as logic
import theapp.models as models


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
        now = time.time()
        new_user = models.FeedUser(user_name=username, user_token=token, url=url, trello_member_id=trello_member_id, created=now, last_access=now)
        new_user.save()
                
        returned_user = logic.get_or_create_user(None, None, trello_member_id, None)
        
        self.assertEqual(returned_user.user_name, user_name)
        self.assertEqual(returned_user.user_token, token)
        self.assertEqual(returned_user.url, url)
        self.assertEqual(returned_user.created, now)
        
    