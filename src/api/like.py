from flask.globals import request
from action.user_checkpoint import get_user_checkpoint
from action.user import get_user
from api.common_lib import authorization_fail, authorize
from action.authorization import is_api_key_validated
from action.like import add_like, delete_like as delete_like_action
from flask.helpers import jsonify

def new_like():
    """
    (PUT: like)
    Instantiates a new <<CheckpointLike>> from a user on a <<UserCheckpoint>>
    """
    
    #req var
    user_id = request.form.get("user_id")
    signature = request.form.get("signature")
    user_checkpoint_id = request.form.get("user_checkpoint_id")
    
    #generated var
    verb = "put"
    noun = "like"
    user = get_user(user_id)
    user_checkpoint = get_user_checkpoint(user_checkpoint_id)
    access_token = user.access_token
    
    #authorization check
    if not is_api_key_validated(access_token, user_id, signature, verb, noun):
        return authorization_fail()
    
    like = add_like(user, user_checkpoint)
    
    return jsonify({
                    "status": "ok",
                    "result": {
                               "like_id": like.id, 
                               }
                    })
    
def delete_like():
    """
    (DELETE: like)
    Deletes an existing <<CheckpointLike>> between a user and a <<UserCheckpoint>>
    if it exists
    """
    #req var
    
    user_id = request.args.get("user_id")
    signature = request.args.get("signature")
    user_checkpoint_id = request.args.get("user_checkpoint_id")
    
    
    #generated var
    verb = "delete"
    noun = "like"
    user = get_user(user_id)
    user_checkpoint = get_user_checkpoint(user_checkpoint_id)
    access_token = user.access_token
    
    #authorization check
    if not is_api_key_validated(access_token, user_id, signature, verb, noun):
        return authorization_fail()

    delete_like_action(user, user_checkpoint)
    
    return jsonify({
                    "status": "ok",
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    
    app.add_url_rule('/like/', 
                     "new_like", new_like, methods=['PUT'])
    app.add_url_rule('/like/', 
                     "delete_like", delete_like, methods=['DELETE'])