#===============================================================================
# unit tests for share action layer
#===============================================================================

from facebook.facebook import get_app_access_token, create_test_user,\
    make_friend_connection, get_wall_posts
from local_config import APP_ID, APP_SECRET
from action.share import share
from action.user_checkpoint import add_checkpoint_to_user
from action.user import save_user
from action.checkpoint import add_checkpoint
from action.location import add_location
from tests.action.test_checkpoint import CheckpointTests
import time
from tests.util.test_base import TestBase

class ShareTests(TestBase):
    
    def test_share(self):
        """
        Tests the share function in the share layer if it does work as expected
        """
        
        #create and save facebook (test) user_a and user_b
        test_user_a = self.create_facebook_test_user()
        test_user_b = self.create_facebook_test_user()
        fb_user_info_a, user_a = save_user(test_user_a["access_token"], "someauthcode")
        fb_user_info_b, user_b = save_user(test_user_b["access_token"], "someauthcode")
        make_friend_connection(user_a.facebook_user.id, user_b.facebook_user.id, user_a.access_token, user_b.access_token)
        
        #create mock checkpoint and add it to user_a
        checkpoint = add_checkpoint(*CheckpointTests.mock_checkpoint_data(user_a.id))
        user_checkpoint  = add_checkpoint_to_user(user_a, checkpoint)
        
        #share checkpoint from user_a to user_b
        share(user_a, user_b, user_checkpoint)
        
        #assert
        print test_user_a