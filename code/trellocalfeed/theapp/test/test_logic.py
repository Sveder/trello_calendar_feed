import json

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
        
        
    