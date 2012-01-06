#===============================================================================
# User (and Facebook auth) API endpoints
#===============================================================================
from flask.helpers import jsonify
from facebook.facebook import get_user_access_token
from local_config import APP_ID, APP_SECRET
from flask.globals import request
from action.authorization import gen_api_key
from action.user import save_user, get_friends

def user_login():
    """
    (PUT: user)
    Method to handle when a user authenticates (from Facebook), be it a new user, or recurring user
    """

    fb_code = request.form.get("fb_code", None)
    access_token = request.form.get("access_token", None)
    
    if access_token is None:
        access_token = get_user_access_token(fb_code, APP_ID, APP_SECRET)
    
    fb_user_info, user = save_user(access_token, fb_code)
    api_key = gen_api_key(access_token, user.id)

    friends_obj = get_friends(user, exclude_self=True)
    friends_lis = [{"user_id": f.id,
                    "facebook_user_id": f.facebook_user_id,
                    "full_name": f.facebook_user.name,
                    } for f in friends_obj]

    return jsonify({"status": "ok",
                    "result": {
                        "user": {
                                 "id": user.id,
                                 },
                        "friends": friends_lis,
                        "facebook_user_id": fb_user_info.id,
                        "api_key": api_key,
                    }
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user/',
                     "user_login", user_login, methods=['PUT'])
