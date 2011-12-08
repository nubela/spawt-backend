import unittest
from ctrleff import get_app
import tempfile
import os
from local_config import APP_ID, APP_SECRET
from facebook.facebook import get_app_access_token, create_test_user,\
    delete_all_test_users

class TestBase(unittest.TestCase):
    
    def setUp(self):
        self.app = get_app()
        #declare testing state
        self.app.config["TESTING"] = True
        self.db, self.app.config["DATABASE"] = tempfile.mkstemp()
        
        #spawn test client
        self.client = self.app.test_client()
        
    def tearDown(self):
        os.close(self.db)
        os.unlink(self.app.config["DATABASE"])
        
        #cleanup facebook test users
        if hasattr(self,"has_facebook_test_user"):
            app_xs_token = get_app_access_token(APP_ID, APP_SECRET)
            #delete_all_test_users(APP_ID, self.get_app_access_token())
    
    def get_app_access_token(self):
        if not hasattr(self, "app_xs_token"):
            self.app_xs_token = get_app_access_token(APP_ID, APP_SECRET)
        return self.app_xs_token
    
    def create_facebook_test_user(self):
        self.has_facebook_test_user = True
        return create_test_user(APP_ID, self.get_app_access_token())