#===============================================================================
# api layer for user stats
# user stats include: liked checkpoints count, reshared checkpoints count
#===============================================================================
from action.like import get_likes_user
from api.common_lib import authorize, authorization_fail
from flask.globals import request
from action.user import get_user
from action.share import get_shares_user
from flask.helpers import jsonify

def get_stats():
    user_id = request.args.get("user_id")
    signature = request.args.get("signature")
    
    if not authorize("get", "stats", user_id, signature):
        return authorization_fail()
    
    #generated
    user_obj = get_user(user_id)
    
    liked_cp = get_likes_user(user_obj)
    reshared_cp = get_shares_user(user_obj)
    
    return jsonify({"status": "ok",
                    "total_likes": len(liked_cp),
                    "total_reshares": len(reshared_cp),
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user/stats/',
                     "get_stats", get_stats, methods=['GET'])