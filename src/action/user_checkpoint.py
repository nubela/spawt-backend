#===============================================================================
# UserCheckpoint action layer 
#===============================================================================
from util.geo import bounding_box, proximity_sort, distance_between_points
from sqlalchemy.sql.expression import and_, or_, union_all, alias, desc
from action.user import get_friends
from collections import namedtuple
from action.checkpoint import CHECKPOINT_TYPES
from action.common import _get_2_weeks_date_before
from sqlalchemy.orm.util import aliased
from action.like import get_total_likes
import datetime
from action.notification import delete_notifications_w_user_checkpoint

def checkpoint_proximity(user_checkpoints, lat, lon):
    """
    returns a list of a dict containing usercheckpoint id, checkpoint ids, and their proximity 
    from the given lat, lon coordinate
    """
    
    lis = [{"user_checkpoint_id" : ucp.id,
            "checkpoint_id": ucp.checkpoint.id,
            "proximity_in_km": distance_between_points(lat, lon, ucp.checkpoint.latitude, ucp.checkpoint.longitude),
            } for ucp in user_checkpoints]
    return lis

def get_user_checkpoint(id):
    """
    gets UserCheckpoint record by id
    """
    from db import UserCheckpoint, db
    cp = UserCheckpoint.query.filter_by(id=id)
    if cp.count() > 0:
        return cp.first()
    return None

def get_user_checkpoint_attr(user_obj, checkpoint_obj):
    """
    gets UserCheckpoint record given supplied args
    """
    from db import UserCheckpoint, db
    cp = UserCheckpoint.query.filter_by(user_id = user_obj.id, checkpoint_id = checkpoint_obj.id)
    if cp.count() > 0:
        return cp.first()
    return None

def remove_checkpoint_from_user(user_obj, checkpoint_obj):
    from db import db
    
    #ensure that user does own the user_checkpoint
    user_checkpoint_obj = get_user_checkpoint_attr(user_obj, checkpoint_obj)
    
    #delete notifications
    delete_notifications_w_user_checkpoint(user_checkpoint_obj)
    
    if not user_checkpoint_obj is None:
        delete_notifications_w_user_checkpoint(user_checkpoint_obj)
        db.session.delete(user_checkpoint_obj)
        db.session.commit()
    
def add_checkpoint_to_user(user_obj, checkpoint_obj):
    """
    Adds a record to the db table to reflect an addition of an NEW Checkpoint 
    to a user's repertoir of Checkpoints
    """
    ucp = get_user_checkpoint_attr(user_obj, checkpoint_obj)
    if not ucp is None:
        return ucp
        
    from db import UserCheckpoint, db
    
    user_checkpoint = UserCheckpoint()
    user_checkpoint.user_id = user_obj.id
    user_checkpoint.checkpoint_id = checkpoint_obj.id
    user_checkpoint.date_added = datetime.datetime.now()
    
    db.session.add(user_checkpoint)
    db.session.commit()
    
    return user_checkpoint
    
def add_existing_checkpoint_to_user(user_obj, user_checkpoint_obj):
    """
    Duplicates a record of an instance of <<UserCheckpoint>> and gives it to
    the provided <<User>>.
    
    Also recursively duplicates corresponding <<UserCheckpointOptions>> and gives it to the
    duplicated instance of <<UserCheckpoint>>
    """
    
    ucp = get_user_checkpoint_attr(user_obj, user_checkpoint_obj.checkpoint)
    if not ucp is None:
        return ucp
    
    from db import UserCheckpoint, UserCheckpointOptions, db
    
    #duplicate UserCheckpoint
    duplicated_ucp = UserCheckpoint()
    duplicated_ucp.user_id = user_obj.id
    duplicated_ucp.checkpoint_id = user_checkpoint_obj.checkpoint_id
    duplicated_ucp.date_added = datetime.datetime.now()
    db.session.add(duplicated_ucp)
    
    #duplicate UserCheckpointOptions
    options = UserCheckpointOptions.query.filter_by(user_checkpoint_id=user_checkpoint_obj.id)
    for opt in options:
        duplicated_opt = UserCheckpointOptions()
        duplicated_opt.user_checkpoint_id = duplicated_ucp.id
        duplicated_opt.name = opt.name
        duplicated_opt.value = opt.value
        db.session.add(duplicated_opt)
        
    db.session.commit()
    
    return duplicated_ucp
    
def get_nearby_checkpoints(user_obj, point_coord, radius_in_kilometres):
    """
    get UserCheckpoints in a given radius sorted according to proximity
    returns in tuple, (friends_user_checkpoints_list, anonymous_user_checkpoints_list)
    """
    from db import UserCheckpoint, db, Checkpoint
    
    #bounding box
    lat, lon = point_coord[0], point_coord[1]
    
    dlat, dlon = bounding_box(lat, lon, radius_in_kilometres)
    min_lat, max_lat = lat-dlat, lat+dlat
    min_lon, max_lon = lon-dlon, lon+dlon
    
    radius_cond = and_(Checkpoint.latitude <= max_lat,
                       Checkpoint.latitude >= min_lat,
                       Checkpoint.longitude <= max_lon,
                       Checkpoint.longitude >= min_lon
                       )
    
    ucp_in_radius = (db.session.query(UserCheckpoint).
                     join(UserCheckpoint.checkpoint).
                     filter(radius_cond).
                     filter(Checkpoint.demo == False)
                     )
    
    #removing dupes and making sure that the oldest creator always gets credited
    unduped_ucp = {}
    all_ucp = ucp_in_radius.all()
    for ucp in all_ucp:
        key = ucp.checkpoint.id 
        if key in unduped_ucp:
            compared_ucp = unduped_ucp[key]
            if ucp.user_id == user_obj.id:
                unduped_ucp[key] = ucp
            elif ucp < compared_ucp and compared_ucp.user_id != user_obj.id: #older
                unduped_ucp[key] = ucp
        else: unduped_ucp[key] = ucp
    all_ucp = [v for k,v in unduped_ucp.iteritems()]
    
    ucp_namedtuples = _checkpoints_to_location_namedtuples(all_ucp)
    sorted_ucp = proximity_sort((lat, lon), ucp_namedtuples, ucp_in_radius.count())
    
    #separate into friends and anon ucp
    friend_list = get_friends(user_obj)
    friends = []
    anon = []
    for ucp in sorted_ucp:
        if ucp.user_checkpoint.user in friend_list:
            friends += [ucp.user_checkpoint]
        else:
            anon += [ucp.user_checkpoint]
    
    return friends, anon

def sort_checkpoints(ucp_lis, sort_method, **kwargs):
    """
    sorts checkpoints according to method supplied.
    methods available are: newest, nearest, popular
    
    if "nearest" method is chosen, longitude/latitude kw args should be provided.
    """
    sorted_ucp = None
    
    if sort_method == "popular":
        sorted_ucp = sorted(ucp_lis, 
                            key=lambda ucp: get_total_likes(ucp), 
                            reverse=True)
        
    elif sort_method == "nearest":
        lat, lon = kwargs["latitude"], kwargs["longitude"] 
        ucp_namedtuples = _checkpoints_to_location_namedtuples(ucp_lis)
        sorted_ucp = proximity_sort((lat, lon), ucp_namedtuples, len(ucp_namedtuples))
        sorted_ucp = [ucp[1] for ucp in sorted_ucp]
    else: #newest
        sorted_ucp = sorted(ucp_lis, key=lambda ucp: ucp.checkpoint.date_created, reverse=True)
    
    return sorted_ucp

def get_my_checkpoints(user_obj):
    """
    get all UserCheckpoints belonging to a user
    """
    from db import UserCheckpoint
    ucp = UserCheckpoint.query.filter_by(user_id=user_obj.id)
    return ucp.all() 

def get_recent_friend_user_checkpoints(user_obj, limit = None):
    """
    (faux notification) returns Checkpoints that were recently created by friends
    """
    if limit == None:
        limit = 8
    
    from db import UserCheckpoint, db, FacebookUser, User, FriendConnection, Checkpoint
    
    FriendUserCheckpoint, FriendFacebookUser, FriendUser = aliased(UserCheckpoint), aliased(FacebookUser), aliased(User)
    q = (db.session.query(UserCheckpoint).
         join(Checkpoint, Checkpoint.id == UserCheckpoint.checkpoint_id).
         join(FriendUser, FriendUser.id == UserCheckpoint.user_id).
         join(FriendFacebookUser, FriendFacebookUser.id == FriendUser.facebook_user_id).
         join(FriendConnection, FriendConnection.fb_user_to == FriendFacebookUser.id).
         join(FacebookUser, FacebookUser.id == FriendConnection.fb_user_from).
         join(User, User.facebook_user_id == FacebookUser.id).
         filter(User.id == user_obj.id).
         filter(Checkpoint.creator == FriendUser.id).
         filter(Checkpoint.demo == False)
         )
    
    return q.order_by(desc(Checkpoint.date_created)).limit(limit).all()

def search_user_checkpoints(user_obj, search_term):
    """
    Searches both my UserCheckpoints and my friends' with a literal search term.
    Searches a Checkpoint's name, description, and User's (Facebook) name (union)
    """
    from db import UserCheckpoint, db, FacebookUser, User, FriendConnection, Checkpoint
    search_term_with_wildcard = "%"+search_term+"%"
    
    #query that contain my own and my friends' usercheckpoints
    FriendUserCheckpoint, FriendFacebookUser, FriendUser = aliased(UserCheckpoint), aliased(FacebookUser), aliased(User)
    ucp = (db.session.query(UserCheckpoint).
           join(Checkpoint, Checkpoint.id == UserCheckpoint.checkpoint_id).
           join(FriendUser, FriendUser.id == UserCheckpoint.user_id).
           join(FriendFacebookUser, FriendFacebookUser.id == FriendUser.facebook_user_id).
           join(FriendConnection, FriendConnection.fb_user_to == FriendFacebookUser.id).
           join(FacebookUser, FacebookUser.id == FriendConnection.fb_user_from).
           join(User, User.facebook_user_id == FacebookUser.id).
           filter(or_(User.id == user_obj.id, FriendUser.id == user_obj.id)).
           filter(Checkpoint.demo == False)        
           )
    
    name_search = ucp.filter(Checkpoint.name.ilike(search_term_with_wildcard))
    desc_search = ucp.filter(Checkpoint.description.ilike(search_term_with_wildcard))
    fb_name_search = ucp.filter(FriendFacebookUser.name.ilike(search_term_with_wildcard))
    
    result = name_search.union(desc_search).union(fb_name_search)
    
    return result.all()

def user_checkpoint_sanify(ucp_collection):
    """
    sanify a <<UserCheckpoint>> collection for jsonify-ication
    by separating it by Checkpoint Types 
    """
    separated = {}
    for ucp in ucp_collection:
        if ucp.checkpoint.type.lower() in CHECKPOINT_TYPES:
            if ucp.checkpoint.type.lower() in separated:
                separated[ucp.checkpoint.type.lower()] += [ucp.serialize]
            else: 
                separated[ucp.checkpoint.type.lower()] = [ucp.serialize]
    return separated

def _checkpoints_to_location_namedtuples(lis_of_cp):
    """
    converts a collection of user checkpoint objects to location namedtuples (usually) for proximity sorting
    """
    Obj = namedtuple("Obj", ("location", "user_checkpoint"))
    lis = []
    for cp in lis_of_cp:
        lis += [Obj((float(cp.checkpoint.latitude), float(cp.checkpoint.longitude)), cp)]
    return lis