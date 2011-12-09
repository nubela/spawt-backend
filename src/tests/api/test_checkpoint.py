from ctrleff import get_resources_abs_path
from os.path import join
from action.user import save_user
from util.util import random_string
from action.authorization import gen_signature, gen_api_key
from action.location import get_location
import base64
from tests.util.test_base import TestBase

class CheckpointAPITests(TestBase):
    
    def test_new_checkpoint(self):
        """
        test the new_checkpoint API
        """
        
        #create/save user
        authcode = "someauthcode"
        test_user = self.create_facebook_test_user()
        fb_info, user = save_user(test_user["access_token"], authcode)
        
        #prep image file
        image_path = join(get_resources_abs_path(), "test/images/timbre.jpg")
        image_file = open(image_path, "r")
        image = base64.encodestring(image_file.read())
        
        #craft request params
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
        
        #send it
        response = self.client.put("/checkpoint/", data=data)
        assert "user_checkpoint_id" in response.data
        
    def test_new_invalid_checkpoint(self):
        """
        test the new_checkpoint API, with an invalid checkpoint (without expiry/price)
        """
        
        #create/save user
        authcode = "someauthcode"
        test_user = self.create_facebook_test_user()
        fb_info, user = save_user(test_user["access_token"], authcode)
        
        #prep image file
        image_path = join(get_resources_abs_path(), "test/images/timbre.jpg")
        image_file = open(image_path, "r")
        image = base64.encodestring(image_file.read())
        
        #craft request params
        data = {"user_id":user.id,
                "signature": gen_signature(authcode, "put", "checkpoint", gen_api_key(authcode, user.id)),
                "name": random_string(),
                "longitude": 2.0,
                "latitude": 1.0,
                "description": random_string(),
                "image": image,
                "type:": "play", 
                }
        
        #send it
        response = self.client.put("/checkpoint/", data=data)
        assert "Requires at least a price or expiry." in response.data