from flask.globals import request
from action.user import get_user
from action.authorization import is_api_key_validated
from api.common_lib import authorization_fail
from action.user_checkpoint import get_user_checkpoint,\
    add_existing_checkpoint_to_user
from flask.helpers import jsonify

def add_checkpoint_to_catalog():
    """
    (POST: user_checkpoint)
    user likes a Checkpoint from a user and wants to add it into his catalog;
    adds checkpoint to user's catalog
    """
    
    #req vars
    user_id = request.form.get("user_id")
    signature = request.form.get("signature")
    to_add_user_checkpoint_id = request.form.get("user_checkpoint_id")
    
    #generated var
    verb = "post"
    noun = "catalog"
    user = get_user(user_id)
    auth_code = user.auth_code
    
    #authorization check
    if not is_api_key_validated(auth_code, user_id, signature, verb, noun):
        return authorization_fail()
    
    user_checkpoint = get_user_checkpoint(to_add_user_checkpoint_id)
    new_user_cp = add_existing_checkpoint_to_user(user, user_checkpoint)
    
    return jsonify({
                    "status": "ok",
                    "result": {
                               "user_checkpoint_id": new_user_cp.id,
                               },
                    }) 
    
def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/catalog/', 
                     "add_checkpoint_to_catalog", add_checkpoint_to_catalog, methods=['POST'])