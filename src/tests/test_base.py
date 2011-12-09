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
    
    def create_saved_test_user(self):
        from util.util import random_string
        from action.user import save_user
        from collections import namedtuple
        
        #create and save fb user
        authcode = random_string()
        test_user = self.create_facebook_test_user()
        fb_info, user = save_user(test_user["access_token"], authcode)
        
        User = namedtuple("User", ("authcode", "fb_test_user", "fb_info", "user_obj", "checkpoint_obj", "user_checkpoint_obj"))
        return User(authcode, test_user, fb_info, user)
    
    def create_saved_test_user_with_checkpoint(self):
        """
        Creates a test user, with a checkpoint
        """
        from collections import namedtuple
        from util.util import random_string
        from action.user import save_user
        from tests.action.test_checkpoint import CheckpointTests
        from action.checkpoint import add_checkpoint
        from action.user_checkpoint import add_checkpoint_to_user
        
        #create and save fb user
        authcode = random_string()
        test_user = self.create_facebook_test_user()
        fb_info, user = save_user(test_user["access_token"], authcode)
        
        #create user checkpoint
        mock_cp_data = CheckpointTests.mock_checkpoint_data(user.id)
        checkpoint = add_checkpoint(*mock_cp_data)
        user_checkpoint = add_checkpoint_to_user(user, checkpoint)
        
        #create namedtuple to store
        User = namedtuple("User", ("authcode", "fb_test_user", "fb_info", "user_obj", "checkpoint_obj", "user_checkpoint_obj"))
        return User(authcode, test_user, fb_info, user, checkpoint, user_checkpoint)
        