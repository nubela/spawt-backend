#===============================================================================
# User (and Facebook auth) API endpoints
#===============================================================================
from flask.helpers import jsonify
from api.user_lib import save_user, update_social_graph
from facebook.facebook import get_user_access_token
from local_config import APP_ID, APP_SECRET

def user_login(fb_code):
    """
    (PUT: user)
    Method to handle when a user authenticates (from Facebook), be it a new user, or recurring user
    """
    
    access_token = get_user_access_token(fb_code, APP_ID, APP_SECRET)
    fb_user_info = save_user(access_token)
    
    return jsonify({
                    "access_token": access_token,
                    "facebook_info": fb_user_info,
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user/', 
                     "user_login", user_login, methods=['PUT'])
