from flask.globals import request
from action.user import get_user
from action.user_checkpoint import get_user_checkpoint
from action.authorization import is_api_key_validated
from api.common_lib import authorization_fail, authorize
from flask.helpers import jsonify
from action.share import share

def new_share():
    """
    (PUT: checkpoint)
    instantiates a share from a user to his facebook friend (be it a ctrleff user or not)
    """
    
    #req vars
    from_user_id = request.form.get("user_id")
    to_user_id = request.form.get("to_user_id")
    signature = request.form.get("signature")
    user_checkpoint_id = request.form.get("user_checkpoint_id")
    
    #generated var
    verb = "put"
    noun = "share"
    user_from = get_user(from_user_id)
    user_to = get_user(to_user_id)
    user_checkpoint = get_user_checkpoint(user_checkpoint_id)
    
    #authorization check
    if not authorize(verb, noun, user_from.id, signature):
        return authorization_fail()
    
    share(user_from, user_to, user_checkpoint)
    
    return jsonify({
                    "status": "ok"
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    
    app.add_url_rule('/share/', 
                     "new_share", new_share, methods=['PUT'])