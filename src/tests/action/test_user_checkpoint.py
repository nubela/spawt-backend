#===============================================================================
# unit tests for user checkpoint action layer
#===============================================================================
from tests.util.test_base import TestBase
from action.user_checkpoint import get_nearby_checkpoints,\
    add_checkpoint_to_user, get_my_checkpoints,\
    get_recent_friend_user_checkpoints, search_user_checkpoints,\
    sort_checkpoints
from tests.action.test_checkpoint import CheckpointTests
from action.checkpoint import add_checkpoint
from action.like import add_like
import time

class UserCheckpointActionTests(TestBase):

    def test_sort_checkpoints(self):
        """
        tests sort_checkpoints() method
        """
        user = self.create_saved_test_user()
        liker = self.create_saved_test_user()
        
        demo_cp = get_my_checkpoints(user.user_obj)
        
        #create various checkpoints (mocked data) for sorting
        cp_a_data = CheckpointTests.mock_checkpoint_data(user.user_obj.id, (0.0,0.0))
        cp_b_data = CheckpointTests.mock_checkpoint_data(user.user_obj.id, (1.0,1.0))
        cp_c_data = CheckpointTests.mock_checkpoint_data(user.user_obj.id, (2.0,2.0))
        
        #create them
        cp_a = add_checkpoint(*cp_a_data)
        time.sleep(1) #have to sleep since datetime doesnt seem to register millisecond differences
        cp_b = add_checkpoint(*cp_b_data)
        time.sleep(1)
        cp_c = add_checkpoint(*cp_c_data)
        ucp_a = add_checkpoint_to_user(user.user_obj, cp_a)
        ucp_b = add_checkpoint_to_user(user.user_obj, cp_b)
        ucp_c = add_checkpoint_to_user(user.user_obj, cp_c)
        
        #get all ucp
        ucp_lis = get_my_checkpoints(user.user_obj)
        assert len(ucp_lis) == 3 + len(demo_cp)
        
        #like checkpoints
        add_like(liker.user_obj, ucp_b)
        
        #sort nearest
        nearest_ucp = sort_checkpoints(ucp_lis, "nearest", longitude = 0.0, latitude = 0.0)
        assert nearest_ucp[0].id == ucp_a.id
        assert nearest_ucp[1].id == ucp_b.id
        assert nearest_ucp[2].id == ucp_c.id
        
        #sort newest
        newest_ucp = sort_checkpoints(ucp_lis, "newest")
        assert newest_ucp[0].id == ucp_c.id
        assert newest_ucp[1].id == ucp_b.id
        assert newest_ucp[2].id == ucp_a.id
        
        #sort popularity
        popular_ucp = sort_checkpoints(ucp_lis, "popular")
        assert popular_ucp[0].id == ucp_b.id
    
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
        #test demo checkpoints
        user = self.create_saved_test_user()
        demo_cp_count = len(get_my_checkpoints(user.user_obj))
        assert demo_cp_count > 0
        
        user2 = self.create_saved_test_user_with_checkpoint()
        assert len(get_my_checkpoints(user2.user_obj)) == demo_cp_count + 1
        
    def test_get_recent_friend_user_checkpoints(self):
        """
        unit test for get_recent_friend_user_checkpoints()
        """
        user_a = self.create_saved_test_user()
        user_b = self.create_saved_test_user_with_checkpoint()
        user_c = self.create_saved_test_user_with_checkpoint()
        user_d = self.create_saved_test_user_with_checkpoint()
        user_e = self.create_saved_test_user_with_checkpoint()
        
        self.befriend_test_user(user_a, [user_b, user_c, user_d])
        
        recent_ucp = get_recent_friend_user_checkpoints(user_a.user_obj, 2)
        assert len(recent_ucp) == 2
        
        recent_ucp = get_recent_friend_user_checkpoints(user_a.user_obj)
        for ucp in recent_ucp:
            assert user_e.user_checkpoint_obj.id != ucp.id
        
    def test_search_user_checkpoints(self):
        """
        unit test for search_user_checkpoints()
        """
        user_a = self.create_saved_test_user_with_checkpoint()
        user_b = self.create_saved_test_user_with_checkpoint()
        user_c = self.create_saved_test_user_with_checkpoint()
        self.befriend_test_user(user_a, [user_b])
        
        #search user_a facebook name
        user_a_fb_name = user_a.user_obj.facebook_user.name
        res = search_user_checkpoints(user_a.user_obj, user_a_fb_name)
        assert len(res) == 1 and res[0] == user_a.user_checkpoint_obj
        
        #search by desc
        desc = user_b.checkpoint_obj.description
        res = search_user_checkpoints(user_a.user_obj, desc)
        assert len(res) == 1 and res[0] == user_b.user_checkpoint_obj
        
        #search by name
        name = user_b.checkpoint_obj.name
        res = search_user_checkpoints(user_a.user_obj, name)
        assert len(res) == 1 and res[0] == user_b.user_checkpoint_obj