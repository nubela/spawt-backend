#===============================================================================
# Action layer for CheckpointLikes
#===============================================================================
import datetime
from action.notification import add_notification,\
    delete_notifications_w_user_checkpoint, delete_notifications_w_relevance

NOTIFICATION_TYPE = "new_like"

def get_likes_user(user_obj):
    """
    returns all the likes a user has
    """
    from db import CheckpointLike, db, UserCheckpoint, Checkpoint
    
    likes = (db.session.query(CheckpointLike).
             join(CheckpointLike.checkpoint).
             join(UserCheckpoint, UserCheckpoint.checkpoint_id == Checkpoint.id).
             filter(UserCheckpoint.user_id == user_obj.id).
             filter(CheckpointLike.user_id != user_obj.id)
             )
    
    return likes.all()

def get_total_likes_checkpoint(checkpoint_obj):
    """
    get the total count of likes for a user checkpoint obj (given the id)
    """
    from db import CheckpointLike, db
    
    likes = CheckpointLike.query.filter_by(checkpoint_id=checkpoint_obj.id)
    return likes.count()

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

def delete_like(user_obj, user_checkpoint_obj):
    """
    Deletes a like record between a user and a Checkpoint if it exists
    """
    from db import db, Notification
    like_obj = get_like_w_attr(user_obj, user_checkpoint_obj.checkpoint)
    if not like_obj is None:
        delete_notifications_w_relevance("new_like", like_obj.id)
        db.session.delete(like_obj)
        db.session.commit()

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
    like_obj.checkpoint_id = user_checkpoint_obj.checkpoint.id
    like_obj.timestamp = datetime.datetime.now()
    like_obj.user_id = user_obj.id
    
    db.session.add(like_obj)
    db.session.commit()
    
    #add notification
    add_notification(NOTIFICATION_TYPE, user_obj, user_checkpoint_obj.user, like_obj.id, user_checkpoint_obj.id)
    
    return like_obj
    