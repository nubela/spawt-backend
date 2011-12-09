#===============================================================================
# Action layer for Likes
#===============================================================================
import datetime

def get_like(id):
    """
    Gets a Like record from the database given id
    """
    from db import Like, db
    likes = Like.query.filter_by(id=id)
    if likes.count() > 0:
        return likes.first()
    return None

def get_like_w_attr(user_obj, checkpoint_obj):
    """
    Gets a Like record from the database given the supplied arguments
    """
    from db import Like, db
    likes = Like.query.filter_by(user_id=user_obj.id, checkpoint_id = checkpoint_obj.id)
    if likes.count() > 0:
        return likes.first()
    return None

def add_like(user_obj, checkpoint_obj):
    """
    Instantiates a new Like record between a user and a Checkpoint,
    returns it if it already exists
    """
    
    like_obj = get_like_w_attr(user_obj, checkpoint_obj)
    if not get_like_w_attr(user_obj, checkpoint_obj) is None:
        return like_obj
    
    from db import Like, db
    
    like_obj = Like()
    like_obj.checkpoint_id = checkpoint_obj.id
    like_obj.timestamp = datetime.datetime.now()
    like_obj.user_id = user_obj.id
    
    db.session.add(like_obj)
    db.session.commit()
    
    return like_obj
    