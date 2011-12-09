from ctrleff import get_resources_abs_path
from os.path import join
from action.user import save_user
from util.util import random_string
from action.authorization import gen_signature, gen_api_key
import base64
import simplejson
from tests.util.test_base import TestBase

class CatalogAPITests(TestBase):
    
    def test_catalog(self):
        """
        tests add_checkpoint_to_catalog()
        """

        user_with_checkpoint = self.create_saved_test_user_with_checkpoint()
        user_for_catalog_add = self.create_saved_test_user()
        
        data = {"user_id": user_for_catalog_add.user_obj.id,
                "signature": gen_signature(user_for_catalog_add.authcode, 
                                           "post", 
                                           "catalog", 
                                           gen_api_key(user_for_catalog_add.authcode, 
                                                       user_for_catalog_add.user_obj.id)),
                "user_checkpoint_id": user_with_checkpoint.user_checkpoint_obj.id, 
                }
        
        response = self.client.post("/catalog/", data=data)
        assert "ok" in response.data