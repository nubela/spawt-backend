#===============================================================================
# unit tests for Checkpoint action layer
#===============================================================================

from tests.test_base import TestBase
from action.user import save_user
from action.location import add_location
from util.util import random_string
import datetime
from action.checkpoint import add_checkpoint, get_checkpoint

class CheckpointTests(TestBase):

    @staticmethod
    def mock_checkpoint_data(creator_user_id):
        location = add_location(2.0, 3.0)
        name = random_string()
        desc = random_string()
        price = 1.0
        expiry = datetime.datetime.now()
        type = "play"
        image = "bla_image"
        return (creator_user_id, location.id, name, type, image, desc, price, expiry)
    
    def test_add_checkpoint(self):
        """
        Tests the add_checkpoint() functionality by creating a mock checkpoint and saving
        it to a mock user
        """
        #create test user
        test_fb_user = self.create_facebook_test_user()
        fb_user, user = save_user(test_fb_user["access_token"], "someauthcode")
        
        #create mock checkpoint
        mock_cp_data = CheckpointTests.mock_checkpoint_data(user.id)
        checkpoint = add_checkpoint(*mock_cp_data)

        #asserts
        assert not get_checkpoint(checkpoint.id) is None