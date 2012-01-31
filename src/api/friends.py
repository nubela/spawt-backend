#===============================================================================
# friends api layer
#===============================================================================
from api.common_lib import authorize, authorization_fail
from flask.globals import request
from action.user import update_social_graph, get_user, get_friends as get_friends_action
from flask.helpers import jsonify
from action.friend_connection import sanify_friends

def get_friends():
    user_id = request.args.get("user_id")
    signature = request.args.get("signature")
    
    if not authorize("get", "friends", user_id, signature):
        return authorization_fail()
    
    #generated
    user_obj = get_user(user_id)
    
    update_social_graph(user_obj.access_token, user_obj.facebook_user)
    friends = get_friends_action(user_obj, exclude_self=True)
    
    return jsonify({"status": "ok",
                    "friends": sanify_friends(friends),
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user/friends/',
                     "get_friends", get_friends, methods=['GET'])