from flask.globals import request
from action.user import get_user
from action.user_checkpoint import get_user_checkpoint
from action.authorization import is_api_key_validated
from api.common_lib import authorization_fail
from flask.helpers import jsonify
from action.comment import add_comment

def new_comment():
    """
    (PUT: comment)
    Instantiates a new <<Comment>> from a user on a <<UserCheckpoint>>
    """
    
    #req var
    user_id = request.form.get("user_id")
    signature = request.form.get("signature")
    user_checkpoint_id = request.form.get("user_checkpoint_id")
    comment = request.form.get("comment")

    #generated var
    verb = "put"
    noun = "comment"
    user = get_user(user_id)
    user_checkpoint = get_user_checkpoint(user_checkpoint_id)
    auth_code = user.auth_code
    
    #authorization check
    if not is_api_key_validated(auth_code, user_id, signature, verb, noun):
        return authorization_fail()
    
    #comment validation
    if len(comment) > 255:
        return jsonify({
                        "status": "error",
                        "error": "Comment too long",
                        })
        
    comment = add_comment(user, user_checkpoint.checkpoint, comment)
    
    return jsonify({
                    "status": "ok",
                    "result": {
                               "comment_id": comment.id
                               }
                    })
    
def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    
    app.add_url_rule('/comment/', 
                     "new_comment", new_comment, methods=['PUT'])