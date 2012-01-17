from flask.globals import request
from action.user import get_user
from action.checkpoint import get_checkpoint
from api.common_lib import authorize, authorization_fail
from action.user_checkpoint import remove_checkpoint_from_user,\
    add_checkpoint_to_user
from flask.helpers import jsonify

def add_user_checkpoint():
    """
    (PUT: user_checkpoint)
    """
    #req args
    user_id = request.form.get("user_id")
    signature = request.form.get("signature")
    checkpoint_id = request.form.get("checkpoint_id")
    
    if not authorize("put", "user_checkpoint", user_id, signature):
        return authorization_fail()
    
    #generated
    user_obj = get_user(user_id)
    checkpoint_obj = get_checkpoint(checkpoint_id)
    
    user_checkpoint = add_checkpoint_to_user(user_obj, checkpoint_obj)
    
    return jsonify({"status": "ok",
                    "user_checkpoint_id": user_checkpoint.id,
                    })
    
def del_user_checkpoint():
    """
    (DELETE: user_checkpoint)
    """
    #req args
    user_id = request.args.get("user_id")
    signature = request.args.get("signature")
    checkpoint_id = request.args.get("checkpoint_id")
    
    if not authorize("delete", "user_checkpoint", user_id, signature):
        return authorization_fail()
    
    #generated vars
    user_obj = get_user(user_id)
    checkpoint_obj = get_checkpoint(checkpoint_id)
    
    remove_checkpoint_from_user(user_obj, checkpoint_obj)
    
    return jsonify({"status": "ok",
                    })
    
def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user_checkpoint/', 
                     "add_user_checkpoint", add_user_checkpoint, methods=['PUT'])
    
    app.add_url_rule('/user_checkpoint/', 
                     "del_user_checkpoint", del_user_checkpoint, methods=['DELETE'])

