from tests.util.test_base import TestBase
from action.like import add_like
from action.share import add_share
from action.authorization import gen_signature, gen_api_key
import simplejson
import urllib

class StatsApiTest(TestBase):
    
    def test_get_stats(self):
        user = self.create_saved_test_user_with_checkpoint()
        other_user = self.create_saved_test_user()
        
        add_like(other_user.user_obj, user.user_checkpoint_obj)
        add_share(other_user.user_obj, user.user_obj, user.user_checkpoint_obj)
        
        data = {"user_id": user.user_obj.id,
                "signature": gen_signature("get", "stats", gen_api_key(user.user_obj.access_token, user.user_obj.id))}
        
        resp = self.client.get("/user/stats/?" + urllib.urlencode(data))
        json_res = simplejson.loads(resp.data)
        assert json_res["total_likes"] == 1
        assert json_res["total_reshares"] == 1
        