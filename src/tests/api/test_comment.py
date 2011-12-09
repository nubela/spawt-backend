from tests.util.test_base import TestBase
from action.authorization import gen_signature, gen_api_key
from util.util import random_string

class CommentAPITest(TestBase):
    
    def test_new_comment(self):
        """
        Unit Test API for instantiating a new Comment (comment/put)
        """
        test_user_with_checkpoint = self.create_saved_test_user_with_checkpoint()
        annoying_user_that_likes_everything = self.create_saved_test_user()
        
        #prep api call
        data = {"user_id": annoying_user_that_likes_everything.user_obj.id,
                "signature": gen_signature(annoying_user_that_likes_everything.authcode, 
                                           "put", 
                                           "comment",
                                           gen_api_key(annoying_user_that_likes_everything.authcode, 
                                                       annoying_user_that_likes_everything.user_obj.id)),
                "user_checkpoint_id": test_user_with_checkpoint.user_checkpoint_obj.id,
                "comment": random_string(), 
                } 
        
        resp = self.client.put("/comment/", data=data)
        assert "comment_id" in resp.data