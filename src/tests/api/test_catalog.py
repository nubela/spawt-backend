from tests.test_base import TestBase
from ctrleff import get_resources_abs_path
from os.path import join
from action.user import save_user
from util.util import random_string
from action.authorization import gen_signature, gen_api_key
import base64
import simplejson

class CatalogTests(TestBase):
    
    def test_catalog(self):
        """
        tests add_checkpoint_to_catalog()
        """
        
        #create a user that created its own checkpointA
        authcode = "someauthcode"
        test_user = self.create_facebook_test_user()
        fb_info, user = save_user(test_user["access_token"], authcode)
        
        image_path = join(get_resources_abs_path(), "test/images/timbre.jpg")
        image_file = open(image_path, "r")
        
        image = base64.encodestring(image_file.read())
        data = {"user_id":user.id,
                "signature": gen_signature(authcode, "put", "checkpoint", gen_api_key(authcode, user.id)),
                "name": random_string(),
                "longitude": 2.0,
                "latitude": 1.0,
                "description": random_string(),
                "price": 3.0,
                "image": image,
                "type:": "play", 
                }
        
        response = self.client.put("/checkpoint/", data=data)
        assert "user_checkpoint_id" in response.data
        
        #create another user that wants to add checkpointA to its catalog
        response_json = simplejson.loads(response.data)
        user_checkpoint_id_to_add =  response_json["result"]["user_checkpoint_id"]
        
        test_user_b = self.create_facebook_test_user()
        fb_info_b, user_b = save_user(test_user_b["access_token"], authcode)
        
        data = {"user_id": user_b.id,
                "signature": gen_signature(authcode, "post", "catalog", gen_api_key(authcode, user_b.id)),
                "user_checkpoint_id": user_checkpoint_id_to_add 
                }
        
        response = self.client.post("/catalog/", data=data)
        assert "ok" in response.data