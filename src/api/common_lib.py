from flask.helpers import jsonify
from action.authorization import is_api_key_validated
from action.user import get_user
from flask.globals import request

def authorization_fail():
    return jsonify({"error": "Authorization fail.",
                    "status": "error",
                    }), 403
                    
def missing_field_fail():
    return jsonify({"error": "Missing field",
                    "status": "error",
                    }), 403
                    
def authorization_required(verb, noun):
    
    def dec(fn):
        
        #auth vars
        user_id = request.form.get("user_id")
        signature = request.form.get("signature")
        user = get_user(user_id)
        auth_code = user.auth_code
        
        if not is_api_key_validated(auth_code, user_id, signature, verb, noun):
            return authorization_fail()
        
        return fn
    
    return dec

def authorize(verb, noun, user_id, signature):
    #auth vars
    user = get_user(user_id)
    auth_code = user.auth_code
    
    if not is_api_key_validated(auth_code, user_id, signature, verb, noun):
        return authorization_fail()