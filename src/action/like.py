#===============================================================================
# Action layer for CheckpointLikes
#===============================================================================
import datetime
from action.notification import add_notification

NOTIFICATION_TYPE = "new_like"

def get_total_likes(user_checkpoint_obj):
    """
    get the total count of likes for a user checkpoint obj (given the id)
    """
    from db import CheckpointLike, db
    
    likes = CheckpointLike.query.filter_by(checkpoint_id=user_checkpoint_obj.checkpoint.id)
    return likes.count()

def get_like(id):
    """
    Gets a CheckpointLike record from the database given id
    """
    from db import CheckpointLike, db
    likes = CheckpointLike.query.filter_by(id=id)
    if likes.count() > 0:
        return likes.first()
    return None

def get_like_w_attr(user_obj, checkpoint_obj):
    """
    Gets a CheckpointLike record from the database given the supplied arguments
    """
    from db import CheckpointLike, db
    likes = CheckpointLike.query.filter_by(user_id=user_obj.id, checkpoint_id = checkpoint_obj.id)
    if likes.count() > 0:
        return likes.first()
    return None

def add_like(user_obj, user_checkpoint_obj):
    """
    Instantiates a new CheckpointLike record between a user and a Checkpoint,
    returns it if it already exists
    """
    
    checkpoint_obj = user_checkpoint_obj.checkpoint
    
    like_obj = get_like_w_attr(user_obj, checkpoint_obj)
    if not get_like_w_attr(user_obj, checkpoint_obj) is None:
        return like_obj
    
    from db import CheckpointLike, db
    
    like_obj = CheckpointLike()
    like_obj.checkpoint_id = checkpoint_obj.id
    like_obj.timestamp = datetime.datetime.now()
    like_obj.user_id = user_obj.id
    
    db.session.add(like_obj)
    db.session.commit()
    
    #add notification
    add_notification(NOTIFICATION_TYPE, user_obj, user_checkpoint_obj.user, like_obj.id)
    
    return like_obj
    