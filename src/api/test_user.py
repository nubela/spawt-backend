import unittest
from facebook.facebook import create_test_user, get_app_access_token,\
    make_friend_connection
from local_config import APP_ID, APP_SECRET
from ctrleff import init_db, get_app
import tempfile
import os
from action.user import save_user, get_user_from_email, get_friends
from action.friend_connection import get_friend_connection
from tests.util.test_base import TestBase

class UserTests(TestBase):
    
    def a_test_save_user(self):
        #create test user with 3 friends
        app_xs_token = get_app_access_token(APP_ID, APP_SECRET)
        test_user = create_test_user(APP_ID, app_xs_token)
        friend_1 = create_test_user(APP_ID, app_xs_token)
        friend_2 = create_test_user(APP_ID, app_xs_token)
        friend_3 = create_test_user(APP_ID, app_xs_token)
        make_friend_connection(test_user["id"], friend_1["id"], test_user["access_token"], friend_1["access_token"])
        make_friend_connection(test_user["id"], friend_2["id"], test_user["access_token"], friend_2["access_token"])
        make_friend_connection(test_user["id"], friend_3["id"], test_user["access_token"], friend_3["access_token"])
        
        fb_user_info, user = save_user(test_user["access_token"], "someauthcode") 
        
        #assert that <<User>> records are indeed created
        assert not get_user_from_email(test_user["email"]) is None

        #assert that <<FriendConnection>> records are made
        from db import FriendConnection
        assert FriendConnection.query.filter_by(fb_user_from=user.facebook_user.id).count() == 3    
        
    def a_test_update_social_graph(self):
        user_a = self.create_saved_test_user()
        user_b = self.create_saved_test_user()
        self.befriend_test_user(user_a, [user_b])
        
        from db import FriendConnection
        assert FriendConnection.query.filter_by(fb_user_from=user_a.user_obj.facebook_user.id).count() == 1
        
    def test_get_friends(self):
        user_a = self.create_saved_test_user()
        a_friend = self.create_saved_test_user()
        a_friend_2 = self.create_saved_test_user()
        self.befriend_test_user(user_a, [a_friend, a_friend_2])
        
        all_friends = get_friends(user_a.user_obj)
        
        assert len(all_friends) == (len([a_friend, a_friend_2]) + 1)