from tests.util.test_base import TestBase
from action.authorization import gen_signature, gen_api_key,\
    is_api_key_validated
from api.common_lib import authorize

class AuthorizationTests(TestBase):
    
    def test_authorize_verb(self):
        user = self.create_saved_test_user()
        
        auth_code = user.authcode
        user_id = user.user_obj.id
        api_key = gen_api_key(auth_code, user_id)
        
        client_side_signature_a = gen_signature(auth_code, "get", "noun", api_key)
        client_side_signature_b = gen_signature(auth_code, "not_get", "noun", api_key)
        
        assert is_api_key_validated(auth_code, user_id, client_side_signature_a, "get", "noun")
        assert not is_api_key_validated(auth_code, user_id, client_side_signature_b, "get", "noun")