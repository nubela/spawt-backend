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
from action.checkpoint import add_checkpoint, get_checkpoint as get_checkpoint_action
from action.location import add_location
from action.user_checkpoint import add_checkpoint_to_user,\
    get_nearby_checkpoints, get_my_checkpoints, search_user_checkpoints,\
    user_checkpoint_sanify, sort_checkpoints, get_user_checkpoint,\
    remove_checkpoint_from_user, get_user_checkpoint_attr
from action.share import add_share as share_checkpoint, get_total_shares
import base64
from os.path import join
from action import user_checkpoint
from action.notification import get_my_notifications_by_date,\
    notification_sanify
from rest_client.rest import unserialize_json_datetime
from action.comment import comment_sanify, get_checkpoint_comments
from collections import namedtuple
from action.like import get_total_likes, get_like_w_attr

def del_checkpoint():
    """
    (DELETE: checkpoint)
    """
    #req args
    user_id = request.args.get("user_id")
    signature = request.args.get("signature")
    user_checkpoint_id = request.args.get("checkpoint_id")
    
    #generated vars
    user_obj = get_user(user_id)
    checkpoint_obj = get_checkpoint_action(user_checkpoint_id)
    
    if not authorize("delete", "checkpoint", user_id, signature):
        return authorization_fail()
    
    remove_checkpoint_from_user(user_obj, checkpoint_obj)
    
    return jsonify({"status": "ok",
                    })

def get_checkpoint():
    """
    (GET: checkpoint)
    """
    type = request.args.get("type")
    user_id = request.args.get("user_id")
    signature = request.args.get("signature")
    
    if not authorize("get", "checkpoint", user_id, signature):
        return authorization_fail()
    
    if type == "search":
        user_checkpoints = _search_checkpoints()
        return jsonify({"checkpoints": user_checkpoint_sanify(user_checkpoints),
                        "status": "ok", 
                        })
        
    elif type == "near":
        friends_ucp, anon_ucp, notifications = _checkpoints_near_me()
        return jsonify({"friends_checkpoints": user_checkpoint_sanify(friends_ucp),
                        "anon_checkpoints": user_checkpoint_sanify(anon_ucp),
                        "notifications": notification_sanify(notifications),
                        "status": "ok", 
                        })
        
    elif type == "mine":
        user_checkpoints = _my_checkpoints()
        return jsonify({"checkpoints": user_checkpoint_sanify(user_checkpoints),
                        "status": "ok", 
                        })
        
    else:
        #single checkpoint info
        res = _checkpoint_details()
        return jsonify({
                        "total_likes": res.total_likes,
                        "total_shares": res.total_shares,
                        "current_user_like": res.current_user_like,
                        "comments": comment_sanify(res.comments),
                        "user": res.user,
                        "checkpoint": res.user_checkpoint_obj.serialize,
                        "status": "ok",
                        })

def _checkpoint_details():
    """
    Gets detailed information about a (User)Checkpoint given its id.   
    """
    CheckpointDetail = namedtuple("CheckpointDetail", 
                                  ("user_checkpoint_obj", 
                                   "total_likes",
                                   "total_shares",
                                   "current_user_like",
                                   "comments",
                                   "user",                                   
                                   ))
    
    user_id = request.args.get("user_id")
    user_checkpoint_id = request.args.get("user_checkpoint_id")
    user_obj = get_user(user_id)
    
    user_checkpoint_obj = get_user_checkpoint(user_checkpoint_id)
    total_likes = get_total_likes(user_checkpoint_obj)
    total_shares = get_total_shares(user_checkpoint_obj)
    current_user_like = (not get_like_w_attr(user_obj, user_checkpoint_obj.checkpoint) is None)
    comments = get_checkpoint_comments(user_checkpoint_obj.checkpoint)
    checkpoint_user_obj = user_checkpoint_obj.user
    user = {"name": checkpoint_user_obj.facebook_user.name,
            "facebook_portrait_url": "https://graph.facebook.com/%s/picture" % checkpoint_user_obj.facebook_user.id,
            }
    
    res = CheckpointDetail(user_checkpoint_obj,
                           total_likes,
                           total_shares,
                           current_user_like,
                           comments,
                           user
                           )
    return res

def _search_checkpoints():
    """
    A simple implementation of keyword search for Checkpoint.
    Append a wildcard to the left and right of the phrase, and search
    Checkpoint's Description, Name, and User's name (Facebook name) 
    """
    user_id = request.args.get("user_id")
    search_term = request.args.get("keyword").strip()
    user = get_user(user_id)
    
    search_results = search_user_checkpoints(user, search_term)
    return search_results    

def _checkpoints_near_me():
    """
    return checkpoints given a location, from both friends/anonymous
    as well as notifications on new comments, etc.
    """
    user_id = request.args.get("user_id")
    point_coord = float(request.args.get("latitude")), float(request.args.get("longitude"))
    radius = float(request.args.get("radius", 2))
    user = get_user(user_id) 
    
    friends_ucp, anon_ucp = get_nearby_checkpoints(user, point_coord, radius)
    notifications = get_my_notifications_by_date(user)
                                                     
    return friends_ucp, anon_ucp, notifications
    
def _my_checkpoints():
    """
    return all user checkpoints that belong to user
    as well as notifications on new comments, etc.
    """
    user_id = request.args.get("user_id")
    user = get_user(user_id)
    sort_method = request.args.get("sort_by", "newest") #can be newest, nearest, popular
    
    user_checkpoints = get_my_checkpoints(user)
    sort_checkpoints(user_checkpoints, sort_method, 
                     longitude=float(request.args.get("longitude", 0.0)),
                     latitude=float(request.args.get("latitude", 0.0))
                     )
    
    return user_checkpoints 

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
    image_encoded = request.form.get("image", None)
    type = request.form.get("type")
    share = request.form.get("share", None)
    facebook_post = request.form.get("facebook_post", False)
    image = None
    if image_encoded is None:
        image = request.files["image"]
    
    #generated vars
    verb = "put"
    noun = "checkpoint"
    user = get_user(user_id)
    expiry_datetime = None
    if expiry:
        expiry_datetime = unserialize_json_datetime(expiry)
    
    if not authorize(verb, noun, user_id, signature):
        print "fail"
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
    
    if image_encoded is None:
        img_file_name = save_file(image, ".jpg", str(user.id), upload_dir, encoded=False)
    else: 
        img_file_name = save_file(image_encoded, ".jpg", str(user.id), upload_dir)
    
    checkpoint = add_checkpoint(user_id, name, type, img_file_name, longitude, latitude, description, price, expiry_datetime)
    user_checkpoint  = add_checkpoint_to_user(user, checkpoint)
    
    #dispatch shares
    if not share is None:
        user_ids_to_share = simplejson.loads(share)
        for uid in user_ids_to_share:
            user_to = get_user(uid)
            share_checkpoint(user, user_to, user_checkpoint)
    
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
    
    app.add_url_rule('/checkpoint/', 
                     "del_checkpoint", del_checkpoint, methods=['DELETE']) 