from tests.util.test_base import TestBase
from action.authorization import gen_api_key, gen_signature
import urllib
import simplejson

class UserCheckpointAPITests(TestBase):
    
    def test_del_user_checkpoint(self):
        """
        unit test for (delete:user_checkpoint) 
        """
        user = self.create_saved_test_user_with_checkpoint()
        
        data = {"user_id": user.user_obj.id,
                "signature": gen_signature("delete", "user_checkpoint", gen_api_key(user.user_obj.access_token, user.user_obj.id)),
                "checkpoint_id": user.user_checkpoint_obj.checkpoint_id,
                }
        
        response = self.client.delete("/user_checkpoint/?" + urllib.urlencode(data))
        json_res = simplejson.loads(response.data)
        
        assert json_res["status"] == "ok" 
    
    def test_add_user_checkpoint(self):
        """
        unit test for (put:user_checkpoint)
        """
        user_a = self.create_saved_test_user_with_checkpoint()
        user_b = self.create_saved_test_user()
        
        data = {"user_id": user_b.user_obj.id,
                "signature": gen_signature("put", "user_checkpoint",
                                           gen_api_key(user_b.user_obj.access_token, user_b.user_obj.id)),
                "checkpoint_id": user_a.checkpoint_obj.id,
                }
        
        response = self.client.put("/user_checkpoint/", data=data)
        assert "ok" in response.data