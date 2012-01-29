import datetime 
from action.common import _get_2_weeks_date_before
from sqlalchemy.sql.expression import desc

NOTIFICATION_TYPES = ("new_like", "new_comment", "new_share")

def add_notification(type, from_user, to_user, obj_id, user_checkpoint_id = None):
    
    #make sure its not a self-notification
    if from_user.id == to_user.id:
        return None
    
    from db import Notification, db
    
    new_notification = Notification()
    new_notification.type = type
    new_notification.from_user_id = from_user.id
    new_notification.affected_user_id = to_user.id
    new_notification.relevant_id = obj_id
    new_notification.timestamp = datetime.datetime.now()
    new_notification.user_checkpoint_id = user_checkpoint_id
    
    db.session.add(new_notification)
    db.session.commit()
    
    return new_notification

def delete_notifications_w_relevance(type, relevant_obj_id):
    """
    deletes notifications that involves the stated user_checkpoint
    """
    from db import db, Notification
    relevant_notifications = Notification.query.filter_by(relevant_id=relevant_obj_id, type=type).all()
    for n in relevant_notifications:
        db.session.delete(n)
    db.session.commit()

def delete_notifications_w_user_checkpoint(ucp_obj):
    """
    deletes notifications that involves the stated user_checkpoint
    """
    from db import db, Notification
    relevant_notifications = Notification.query.filter_by(user_checkpoint_id = ucp_obj.id).all()
    for n in relevant_notifications:
        db.session.delete(n)
    db.session.commit()

def get_my_notifications_by_date(user_obj, cut_off_date = None):
    """
    return most recent <<Notification>> of various types before a certain cut off date 
    """
    if cut_off_date is None:
        cut_off_date = _get_2_weeks_date_before()
    
    from db import db, Notification
    notifications = Notification.query.filter_by(affected_user_id = user_obj.id).filter(Notification.timestamp > cut_off_date).order_by(desc(Notification.timestamp))
    return notifications.all()

def get_my_notifications(user_obj, limit=None):
    from db import db, Notification
    
    if limit is None:
        limit = 100
    
    notifications = Notification.query.filter_by(affected_user_id = user_obj.id).order_by(desc(Notification.timestamp)).limit(limit)
    return notifications.all()

def notification_sanify(notification_collection):
    """
    sanify a queryset of Notifications for json.
    Separate Notification objects into various notification types.
    """
    return [n.serialize for n in notification_collection]

def describe_notification(notification_obj): 
    """
    Describes a notification in a human understandable manner.
    Returns a dictionary that
     
    - contains a text string that will explain
    what this notification is about;
    - a url to the checkpoint image
    - and the id of the relevant user checkpoint obj 
    """
    from action.like import get_like
    from action.comment import get_comment
    from action.share import get_share
    from action.user_checkpoint import get_user_checkpoint_attr
    from action.serve import get_checkpoint_img_url
    
    ucp_id = None
    txt = ""
    ucp_url = None
    
    relevant_user_name = notification_obj.from_user.facebook_user.name
    
    if notification_obj.type == "new_like":
        #format: XXX likes your Checkpoint: "Chicken Rice"
        like_obj = get_like(notification_obj.relevant_id)
        user_checkpoint_obj = get_user_checkpoint_attr(notification_obj.affected_user, like_obj.checkpoint)
        
        ucp_id = user_checkpoint_obj.id
        ucp_url = get_checkpoint_img_url(like_obj.checkpoint)
        txt = "%s likes your Checkpoint: %s" % (relevant_user_name, like_obj.checkpoint.name)
                
    elif notification_obj.type == "new_comment":
        #format: XXX commented on Checkpoint: "Chicken Rice"
        comment_obj = get_comment(notification_obj.relevant_id)
        user_checkpoint_obj = get_user_checkpoint_attr(notification_obj.affected_user, comment_obj.checkpoint)
        ucp_id = user_checkpoint_obj.id
        ucp_url = get_checkpoint_img_url(user_checkpoint_obj.checkpoint)
        txt = "%s commented on Checkpoint: %s" % (relevant_user_name, comment_obj.checkpoint.name)
        
    elif notification_obj.type == "new_share":
        #format: XXX recommends you to check out a Checkpoint: "Chicken Rice"
        share_obj = get_share(notification_obj.relevant_id)
        user_checkpoint_obj = share_obj.user_checkpoint
        ucp_id = user_checkpoint_obj.id
        ucp_url = get_checkpoint_img_url(user_checkpoint_obj.checkpoint)
        txt = "%s recommends you to check out a Checkpoint: %s" % (relevant_user_name, user_checkpoint_obj.checkpoint.name)
        
    return {"notification_text": txt,
            "checkpoint_img_url": ucp_url,
            "user_checkpoint_id": ucp_id,
            }