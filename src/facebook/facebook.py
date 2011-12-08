#===============================================================================
# utils to interface with facebook opengraph
#===============================================================================
from rest_client.rest import Request as ReSTRequest
from util.util import random_letters

FACEBOOK_GRAPH_API_URL = "graph.facebook.com"
PERMISSIONS = "email,offline_access,publish_stream"
TEST_PERMISSIONS = "email,offline_access,publish_stream,read_stream"
API_CACHE = {}  

def get_wall_posts(app_access_token, profile_id):
    """
    (For unit tests)
    Gets wall posts from a test user
    branch: /PROFILE_ID/feed
    """
    param = {"access_token": app_access_token,
             }
    request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "GET", param)
    request.send("/"+profile_id+"/feed")
    return request.json_data()

def post_on_wall(app_access_token, profile_id, message, picture=None, link=None, name=None, caption=None):
    """
    Posts a wall feed. 
    branch: /PROFILE_ID/feed
    """
    param = {"access_token": app_access_token,
             "message": message,
             "link": link,
             "name": name,
             "caption": caption,
             }
    print param
    request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "POST", param)
    request.send("/"+profile_id+"/feed")

def get_app_access_token(app_id, app_secret):
    """
    Authenticates appl
    Exchanges app's secret to get an (app) access token
    """
    param = {
             "client_id": app_id,
             "client_secret": app_secret,
             "grant_type": "client_credentials",
             }
    
    app_auth_request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "get", param)
    app_auth_request.send("/oauth/access_token")
    result = app_auth_request.decoded_data()
    return result["access_token"]

def get_user_access_token(code, app_id, app_secret, redirect_uri="http://ctrleff.com/"):
    """
    Authenticates an app with a user's code;
    Exchanges a user's auth code and to an access token
    """
    
    #build param with app's data
    param = {
             "client_id":app_id,
             "client_secret":app_secret,
             "redirect_uri":redirect_uri,
             "code":code,
             }
    
    app_auth_request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "get", param)
    app_auth_request.send("/oauth/access_token")
    result = app_auth_request.decoded_data()
    return result["access_token"]

def create_test_user(app_id, app_xs_token):
    param = {
             "installed":"true",
             "name": random_letters()[:5],
             "method": "post",
             "access_token": app_xs_token,
             "permissions": TEST_PERMISSIONS,
             }
    
    request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "post", param)
    request.send("/%s/accounts/test-users" % app_id)
    result = request.json_data()
    return result

def make_friend_connection(user1_id, user2_id, user1_xs_token, user2_xs_token):
    request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "post", param = {"method": "post", "access_token": user1_xs_token})
    request2 = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "post", param = {"method": "post", "access_token": user2_xs_token})
    request.send("/%s/friends/%s" % (user1_id, user2_id))
    request2.send("/%s/friends/%s" % (user2_id, user1_id))

def delete_test_user(user_id, app_xs_token):
    request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "delete", param = {"access_token": app_xs_token})
    request.send("/%s" % user_id)
    result = request.json_data()
    return result

def delete_all_test_users(app_id, app_xs_token):
    request = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "get", param = {"access_token": app_xs_token})
    request.send("/%s/accounts/test-users" % app_id)
    data = request.json_data()
    test_users = data["data"]
    for user in test_users:
        delete_test_user(user["id"], app_xs_token) 

class FacebookApi:
    
    access_token = None
    
    def __init__(self, access_token):
        self.access_token = access_token
        API_CACHE[access_token] = self

    @staticmethod
    def new(access_token):
        return API_CACHE.get(access_token, FacebookApi(access_token))

    def get_info(self, rehash=False):
        if not rehash and hasattr(self, "info"):
            return self.info
        
        req = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "get", {
                                                          "access_token": self.access_token,
                                                          })
        req.send("/me")
        self.info = req.json_data()
        self.info_raw = req.data
        return self.info

    def get_friends(self, rehash=False):
        if not rehash and hasattr(self, "friends"):
            return self.friends
        
        req = ReSTRequest.new(FACEBOOK_GRAPH_API_URL, "get", {
                                                          "access_token": self.access_token,
                                                          "offset": 0,
                                                          "format": "json",
                                                          "limit": 50000,                                                          
                                                          })
        req.send("/me/friends")
        self.friends = req.json_data()
        self.friends_raw = req.data
        return self.friends

