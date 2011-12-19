#===============================================================================
# unit tests for user checkpoint action layer
#===============================================================================
from tests.util.test_base import TestBase
from action.user_checkpoint import get_nearby_checkpoints,\
    add_checkpoint_to_user, get_my_checkpoints,\
    get_recent_friend_user_checkpoints
from tests.action.test_checkpoint import CheckpointTests
from action.checkpoint import add_checkpoint

class UserCheckpointActionTests(TestBase):
    
    def test_get_nearby_checkpoints(self):
        """
        unit tests get_nearby_checkpoints
        """
        #group a
        a_user1 = self.create_saved_test_user()
        a_user2 = self.create_saved_test_user()
        self.befriend_test_user(a_user1, [a_user2])
        
        #anon users
        anon_user1 = self.create_saved_test_user()
        
        #create checkpoints in group a
        checkpoint_a_data = CheckpointTests.mock_checkpoint_data(a_user1.user_obj.id, (999.9, 999.9))
        a1_checkpoint = add_checkpoint(*checkpoint_a_data)
        a1_ucp = add_checkpoint_to_user(a_user1.user_obj, a1_checkpoint)
        
        checkpoint_b_data = CheckpointTests.mock_checkpoint_data(a_user2.user_obj.id, (-999.9, -999.9))
        a2_checkpoint = add_checkpoint(*checkpoint_b_data)
        a2_ucp = add_checkpoint_to_user(a_user2.user_obj, a2_checkpoint)
        
        checkpoint_c_data = CheckpointTests.mock_checkpoint_data(anon_user1.user_obj.id, (999.9, 999.9))
        a3_checkpoint = add_checkpoint(*checkpoint_c_data)
        a3_ucp = add_checkpoint_to_user(anon_user1.user_obj, a3_checkpoint)
        
        #verification
        friends_ucp, anon_ucp = get_nearby_checkpoints(a_user1.user_obj, (999.9, 999.9), 0.1)
        
        assert a1_ucp in friends_ucp
        assert not a2_ucp in friends_ucp
        assert a3_ucp in anon_ucp
        
    def test_my_checkpoints(self):
        """
        unit test for get_my_checkpoints()
        """
        user = self.create_saved_test_user_with_checkpoint()
        assert len(get_my_checkpoints(user.user_obj)) == 1
        
    def test_get_recent_friend_user_checkpoints(self):
        """
        unit test for get_recent_friend_user_checkpoints()
        """
        user_a = self.create_saved_test_user()
        user_b = self.create_saved_test_user_with_checkpoint()
        self.befriend_test_user(user_a, [user_b])
        
        recent_ucp = get_recent_friend_user_checkpoints(user_a.user_obj)
        
        assert len(recent_ucp) == 1