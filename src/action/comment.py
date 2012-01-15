#===============================================================================
# Action layer for Comment
#===============================================================================
import datetime
from action.notification import add_notification

NOTIFICATION_TYPE = "new_like"

def get_checkpoint_comments(checkpoint_obj):
    from db import Comment
    all_comments = Comment.query.filter_by(checkpoint_id = checkpoint_obj.id)
    return all_comments

def get_comment(id):
    """
    Gets the <<Comment>> object with the supplied id
    """
    
    from db import Comment
    
    comments = Comment.query.filter_by(id=id)
    if comments.count() > 0:
        return comments.first()
    return None


def add_comment(user_obj, user_checkpoint_obj, comment):
    """
    Instantiates a new comment for a user on a Checkpoint
    """
    
    from db import db, Comment
    
    checkpoint_obj = user_checkpoint_obj.checkpoint
    
    comment = Comment()
    comment.checkpoint_id = checkpoint_obj.id
    comment.user_id = user_obj.id
    comment.comment = comment
    comment.timestamp = datetime.datetime.now() 

    db.session.add(comment)
    db.session.commit()
    
    #add notification
    add_notification(NOTIFICATION_TYPE, user_obj, user_checkpoint_obj.user, comment.id)
    
    return comment

def del_comment(id):
    """
    Deletes the <<Comment>> object given its id from the database
    """
    
    from db import db, Comment
    
    comment = get_comment(id)
    
    db.session.delete(comment)
    db.commit()

def comment_sanify(collection):
    return [c.serialize for c in collection]