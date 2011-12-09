from action.authorization import gen_api_key, gen_signature
from action.share import get_share_w_attr
from tests.util.test_base import TestBase

class ShareAPITest(TestBase):
    
    def test_new_share(self):
        """
        tests API for instantiating a new share (share/put)
        """
        
        test_user_with_checkpoint = self.create_saved_test_user_with_checkpoint()
        another_test_user_to_share = self.create_saved_test_user()
        
        data = {"user_id": test_user_with_checkpoint.user_obj.id,
                "to_user_id": another_test_user_to_share.user_obj.id,
                "signature": gen_signature(test_user_with_checkpoint.authcode, "put", "share", 
                                           gen_api_key(test_user_with_checkpoint.authcode, 
                                                       test_user_with_checkpoint.user_obj.id)),
                "user_checkpoint_id": test_user_with_checkpoint.user_checkpoint_obj.id
                }
        
        resp = self.client.put("/share/", data=data)
        assert "ok" in resp.data
        assert not get_share_w_attr(test_user_with_checkpoint.user_obj, 
                                    another_test_user_to_share.user_obj, 
                                    test_user_with_checkpoint.user_checkpoint_obj) is None