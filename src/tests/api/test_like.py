from tests.util.test_base import TestBase
from action.authorization import gen_signature, gen_api_key
import urllib


class LikeAPITest(TestBase):
        
    def test_del_like(self):
        """
        Unit Test API for creating and deleting a CheckpointLike (like:dekete/put)
        """
        test_user_with_checkpoint = self.create_saved_test_user_with_checkpoint()
        annoying_user_that_likes_everything = self.create_saved_test_user()
        
        #prep api call
        data = {"user_id": annoying_user_that_likes_everything.user_obj.id,
                "signature": gen_signature("put", 
                                           "like",
                                           gen_api_key(annoying_user_that_likes_everything.user_obj.access_token, 
                                                       annoying_user_that_likes_everything.user_obj.id)),
                "user_checkpoint_id": test_user_with_checkpoint.user_checkpoint_obj.id, 
                }
        
        data2 = {"user_id": annoying_user_that_likes_everything.user_obj.id,
                "signature": gen_signature("delete", 
                                           "like",
                                           gen_api_key(annoying_user_that_likes_everything.user_obj.access_token, 
                                                       annoying_user_that_likes_everything.user_obj.id)),
                "user_checkpoint_id": test_user_with_checkpoint.user_checkpoint_obj.id, 
                }  
        
        resp = self.client.put("/like/", data=data)
        assert "like_id" in resp.data
        
        resp = self.client.delete("/like/?" + urllib.urlencode(data2))
        assert "ok" in resp.data