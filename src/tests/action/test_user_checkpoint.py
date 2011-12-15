#===============================================================================
# unit tests for user checkpoint action layer
#===============================================================================
from tests.util.test_base import TestBase
from action.user_checkpoint import get_nearby_checkpoints

class UserCheckpointActionTests(TestBase):
    
    def test_get_nearby_checkpoints(self):
        """
        unit tests get_nearby_checkpoints
        """
        user_a_with_friends = self.create_saved_test_user()
        user_b = self.create_saved_test_user()
        user_c = self.create_saved_test_user()
        user_d = self.create_saved_test_user()
        self.befriend_test_user(user_a_with_friends, (user_b, user_c, user_d))
        
        nearby_ucp = get_nearby_checkpoints(user_a_with_friends.user_obj, (0.0,0.0), 99999)
        for ucp in nearby_ucp:
            print ucp 