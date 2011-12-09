from tests.util.test_base import TestBase
from action.authorization import gen_signature, gen_api_key


class LikeAPITest(TestBase):
    
    def test_new_like(self):
        """
        Unit Test API for instantiating a new Like (like/put)
        """
        
        test_user_with_checkpoint = self.create_saved_test_user_with_checkpoint()
        annoying_user_that_likes_everything = self.create_saved_test_user()
        
        #prep api call
        data = {"user_id": annoying_user_that_likes_everything.user_obj.id,
                "signature": gen_signature(annoying_user_that_likes_everything.authcode, 
                                           "put", 
                                           "like",
                                           gen_api_key(annoying_user_that_likes_everything.authcode, 
                                                       annoying_user_that_likes_everything.user_obj.id)),
                "user_checkpoint_id": test_user_with_checkpoint.user_checkpoint_obj.id, 
                } 
        
        resp = self.client.put("/like/", data=data)
        assert "like_id" in resp.data