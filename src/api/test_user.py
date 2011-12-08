import unittest
from facebook.facebook import create_test_user, get_app_access_token,\
    make_friend_connection
from local_config import APP_ID, APP_SECRET
from ctrleff import init_db, get_app
import tempfile
import os
from action.user import save_user

class UserTests(unittest.TestCase):
    
    def setUp(self):
        self.app = get_app()
        #declare testing state
        self.app.config["TESTING"] = True
        self.db, self.app.config["DATABASE"] = tempfile.mkstemp()
        
        #spawn test client
        self.client = self.app.test_client()
        #temp db
        #init_db()
    
    def tearDown(self):
        os.close(self.db)
        os.unlink(self.app.config["DATABASE"])
    
    def test_save_user(self):
        #create test user with 3 friends
        app_xs_token = get_app_access_token(APP_ID, APP_SECRET)
        test_user = create_test_user(APP_ID, app_xs_token)
        friend_1 = create_test_user(APP_ID, app_xs_token)
        friend_2 = create_test_user(APP_ID, app_xs_token)
        friend_3 = create_test_user(APP_ID, app_xs_token)
        make_friend_connection(test_user["id"], friend_1["id"], test_user["access_token"], friend_1["access_token"])
        make_friend_connection(test_user["id"], friend_2["id"], test_user["access_token"], friend_2["access_token"])
        make_friend_connection(test_user["id"], friend_3["id"], test_user["access_token"], friend_3["access_token"])
        
        save_user(test_user["access_token"], "someauthcode") 