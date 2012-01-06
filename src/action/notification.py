import datetime
from action.common import _get_2_weeks_date_before

NOTIFICATION_TYPES = ("new_like", "new_comment", "new_share")

def add_notification(type, from_user, to_user, obj_id, description=None):
    from db import Notification, db
    
    new_notification = Notification()
    new_notification.type = type
    new_notification.from_user_id = from_user.id
    new_notification.affected_user_id = to_user.id
    new_notification.relevant_id = obj_id
    new_notification.description = description
    new_notification.timestamp = datetime.datetime.now()
    new_notification.fresh = True
    
    db.session.add(new_notification)
    db.session.commit()
    
    return new_notification

def get_my_notifications_by_date(user_obj, cut_off_date = None):
    """
    return most recent <<Notification>> of various types before a certain cut off date 
    """
    if cut_off_date is None:
        cut_off_date = _get_2_weeks_date_before()
    
    from db import db, Notification
    notifications = Notification.query.filter(Notification.timestamp > cut_off_date)
    return notifications.all()

def notification_sanify(notification_collection):
    """
    sanify a queryset of Notifications for json.
    Separate Notification objects into various notification types.
    """
    separated = {}
    for n in notification_collection:
        if n.type in NOTIFICATION_TYPES:
            if n.type in separated:
                separated[n.type] += [n.serialize]
            else:
                separated[n.type] = [n.serialize]
    return separated