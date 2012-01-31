from tests.util.test_base import TestBase
from action.authorization import gen_signature, gen_api_key
import urllib
import simplejson

class FriendsApiTest(TestBase):
    
    def test_get_friends(self):
        user = self.create_saved_test_user()
        friend_a, friend_b = self.create_saved_test_user(), self.create_saved_test_user()
        self.befriend_test_user(user, [friend_a, friend_b])
        
        data = {"user_id": user.user_obj.id,
                "signature": gen_signature("get", "friends", gen_api_key(user.user_obj.access_token, user.user_obj.id))}
        
        resp = self.client.get("/user/friends/?" + urllib.urlencode(data))
        json_res = simplejson.loads(resp.data)
        assert len(json_res["friends"]) == 2
        