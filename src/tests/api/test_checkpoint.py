from ctrleff import get_resources_abs_path
from os.path import join
from action.user import save_user
from util.util import random_string
from action.authorization import gen_signature, gen_api_key
from action.location import get_location
import base64
from tests.util.test_base import TestBase
import urllib
from tests.action.test_checkpoint import CheckpointTests
from action.checkpoint import add_checkpoint
from action.user_checkpoint import add_checkpoint_to_user
import simplejson
from action.like import add_like

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
                "signature": gen_signature("put", "checkpoint", gen_api_key(user.access_token, user.id)),
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
                "signature": gen_signature("put", "checkpoint", gen_api_key(user.access_token, user.id)),
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
        
    def test_get_checkpoint_search(self):
        """
        test the search functionality of (get:checkpoint) api 
        """
        user_a = self.create_saved_test_user_with_checkpoint()
        user_b = self.create_saved_test_user_with_checkpoint()
        self.befriend_test_user(user_a, [user_b]) 
        
        #build data for request
        data = {"user_id":user_a.user_obj.id,
                "signature": gen_signature("get", "checkpoint", gen_api_key(user_a.user_obj.access_token, user_a.user_obj.id)),
                "type": "search",
                "keyword": user_b.checkpoint_obj.name, 
                }
        
        response = self.client.get("/checkpoint/?" + urllib.urlencode(data))
        assert "ok" in response.data
        assert user_b.checkpoint_obj.name in response.data
        
    def test_get_checkpoint_near(self):
        """
        test the nearby-checkpoints functionality of (get:checkpoint) api 
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
        
        #build data
        data = {"user_id":a_user1.user_obj.id,
                "signature": gen_signature("get", "checkpoint", gen_api_key(a_user1.user_obj.access_token, a_user1.user_obj.id)),
                "type": "near",
                "latitude": 999.9,
                "longitude": 999.9,
                "radius": 0.1,
                }
        
        response = self.client.get("/checkpoint/?" + urllib.urlencode(data))
        assert "ok" in response.data
        assert a1_ucp.checkpoint.name in response.data
        assert not a2_ucp.checkpoint.name in response.data
        assert a3_ucp.checkpoint.name in response.data
        
    def test_get_checkpoint_mine(self):
        """
        test the my-checkpoints functionality
                getNewCheckpointBean().getUserBean().getUserId()).toString()));y of (get:checkpoint) api
        """
        #create users
        user_a = self.create_saved_test_user_with_checkpoint()
        user_b = self.create_saved_test_user_with_checkpoint()
        self.befriend_test_user(user_a, [user_b])
        
        data = {"user_id":user_a.user_obj.id,
                "signature": gen_signature("get", "checkpoint", gen_api_key(user_a.user_obj.access_token, user_a.user_obj.id)),
                "type": "mine",
                }
        
        response = self.client.get("/checkpoint/?" + urllib.urlencode(data))
        assert "ok" in response.data
        assert user_a.checkpoint_obj.name in response.data
        assert not user_b.checkpoint_obj.name in response.data
        
    def test_get_checkpoint_details(self):
        """
        tests checkpoint detail api
        """
        user_a = self.create_saved_test_user_with_checkpoint()
        user_b = self.create_saved_test_user()
        add_like(user_a.user_obj, user_a.user_checkpoint_obj)
        
        data = {"user_id": user_a.user_obj.id,
                "signature": gen_signature("get", "checkpoint", gen_api_key(user_a.user_obj.access_token, user_a.user_obj.id)),
                "user_checkpoint_id": user_a.user_checkpoint_obj.id,
                }
        
        response = self.client.get("/checkpoint/?" + urllib.urlencode(data))
        json_res = simplejson.loads(response.data)
        assert json_res["current_user_like"] == True
        assert json_res["status"] == "ok"