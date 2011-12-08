#===============================================================================
# User (and Facebook auth) API endpoints
#===============================================================================
from flask.helpers import jsonify
from facebook.facebook import get_user_access_token
from local_config import APP_ID, APP_SECRET
from flask.globals import request
from action.authorization import gen_api_key
from action.user import save_user

def user_login():
    """
    (PUT: user)
    Method to handle when a user authenticates (from Facebook), be it a new user, or recurring user
    """

    fb_code = request.form.get("fb_code")

    access_token = get_user_access_token(fb_code, APP_ID, APP_SECRET)
    fb_user_info, user = save_user(access_token, fb_code)
    api_key = gen_api_key(access_token, user.id)

    return jsonify({"status": "ok",
                    "result": {
                        "user": {
                                 "id": user.id,
                                 },
                        "facebook_info": fb_user_info,
                        "api_key": api_key,
                    }
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user/',
                     "user_login", user_login, methods=['PUT'])
