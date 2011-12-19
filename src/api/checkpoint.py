#===============================================================================
# Checkpoint API Endpoints
#===============================================================================
from flask.globals import request
import datetime
from ctrleff import get_app, get_resources_abs_path
from flask.helpers import jsonify
from api.common_lib import authorization_fail, missing_field_fail,\
    authorization_required, authorize
import simplejson
from action.authorization import is_api_key_validated
from action.user import get_user
from action.checkpoint import add_checkpoint
from action.location import add_location
from action.user_checkpoint import add_checkpoint_to_user,\
    get_nearby_checkpoints, get_my_checkpoints
from action.share import share
import base64
from os.path import join
from action import user_checkpoint

def get_checkpoint():
    """
    (GET: checkpoint)
    """
    authorize("get", "checkpoint")
    
    longitude = request.form.get("type")
    
    if type == "search":
        result = _search_checkpoints()
    elif type == "near":
        result = _checkpoints_near_me()
    elif type == "mine":
        result = _my_checkpoints()
    return missing_field_fail()
    
def _search_checkpoints():
    """
    A simple implementation of keyword search for Checkpoint.
    Append a wildcard to the left and right of the phrase, and search
    Checkpoint's Description, Name, and User's name (Facebook name) 
    """
    user_id = request.form.get("user_id")
    user = get_user(user_id)
    search_term = request.form.get("keyword").strip()
    
    pass    

def _checkpoints_near_me():
    """
    return checkpoints given a location, from both friends/anonymous
    as well as notifications on new comments, etc.
    """
    user_id = request.form.get("user_id")
    user = get_user(user_id)
    point_coord = request.form.get("latitude"), request.form.get("longitude") 
    radius = request.form.get("radius", 2)
    
    nearby_checkpoints = get_nearby_checkpoints(user, point_coord, radius)
    return nearby_checkpoints
    
def _my_checkpoints():
    """
    return all user checkpoints that belong to user
    as well as notifications on new comments, etc.
    """
    user_id = request.form.get("user_id")
    user = get_user(user_id)
    return get_my_checkpoints(user)

def new_checkpoint():
    """
    (PUT: checkpoint) *requires authorization
    creates a barebone checkpoint (just location and image)
    this checkpoint is not complete yet.
    """
    
    #req vars
    user_id = request.form.get("user_id")
    signature = request.form.get("signature")
    name = request.form.get("name")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    description = request.form.get("description", None)
    price = request.form.get("price", None)
    expiry = request.form.get("expiry", None)
    image_encoded = request.form.get("image")
    type = request.form.get("type")
    share = request.form.get("share", None)
    
    #generated vars
    verb = "put"
    noun = "checkpoint"
    user = get_user(user_id)
    auth_code = user.auth_code
    
    #authorization check
    if not is_api_key_validated(auth_code, user_id, signature, verb, noun):
        return authorization_fail()
    
    #checkpoint validation check
    if price is None and expiry is None:
        return jsonify({
                        "status": "error",
                        "error": "Requires at least a price or expiry.",
                        })
    
    #save image
    from util.fileupload import save_file
    upload_dir = join(get_resources_abs_path(), "uploads")
    img_file_name = save_file(image_encoded, ".jpg", str(user.id), upload_dir)
    
    checkpoint = add_checkpoint(user_id, name, type, img_file_name, longitude, latitude, description, price, expiry)
    user_checkpoint  = add_checkpoint_to_user(user, checkpoint)
    
    #dispatch shares
    if not share is None:
        user_ids_to_share = simplejson.loads(share)
        for uid in user_ids_to_share:
            share(user.id, uid, user_checkpoint)
    
    #return success
    return jsonify({
                    "status": "ok",
                    "result": {
                               "user_checkpoint_id": user_checkpoint.id,
                               },
                    })

def update_checkpoint(checkpoint_id, **kwargs):
    """
    (POST: checkpoint)
    updates a checkpoint with its meta info.
    checkpoint will be complete after
    """
    return jsonify({
                    "status": "unimplemented"
                    })

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    
    app.add_url_rule('/checkpoint/', 
                     "new_checkpoint", new_checkpoint, methods=['PUT'])
    
    app.add_url_rule('/checkpoint/', 
                     "get_checkpoints", get_checkpoint, methods=['GET'])