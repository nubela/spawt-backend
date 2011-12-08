import unittest
from ctrleff import get_app
import tempfile
import os
from local_config import APP_ID, APP_SECRET
from facebook.facebook import get_app_access_token, create_test_user
import datetime
import base64
import hmac
from action.user import save_user
from action.authorization import gen_api_key

class CheckpointTests(unittest.TestCase):
    
    def setUp(self):
        self.app = get_app()
        #declare testing state
        self.app.config["TESTING"] = True
        self.db, self.app.config["DATABASE"] = tempfile.mkstemp()
        
        #spawn test client
        self.client = self.app.test_client()
        
    def tearDown(self):
        os.close(self.db)
        os.unlink(self.app.config["DATABASE"])
        
    def test_authorization(self):
        """
        tests the authorization of a rest api call
        """
        #create a user
        app_xs_token = get_app_access_token(APP_ID, APP_SECRET)
        test_user = create_test_user(APP_ID, app_xs_token)
        auth_code = "someauthcode"
        fb_user_info, user = save_user(test_user["access_token"], auth_code)
        user_id = user.id
        api_key = gen_api_key(auth_code, user_id)
        
        #create signature
        signature = "\n".join([auth_code, "put", "checkpoint"])
        encrypted_sig = hmac.new(api_key, signature)
        base64_sig = base64.encodestring(encrypted_sig.hexdigest())
        
        #using user's credentials to access new_checkpoint api
        data = {"signature": base64_sig,
                "user_id": user_id}
        resp = self.client.put("/checkpoint/", data=data)
        