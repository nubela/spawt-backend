#===============================================================================
# action layer for sharing checkpoints via Facebook
#===============================================================================
from facebook.facebook import post_on_wall, get_app_access_token
import datetime
from local_config import APP_ID, APP_SECRET
from action.notification import add_notification

FACEBOOK_SHARE_CAPTION = "Another experience captured by ctrlEFF"
NOTIFICATION_TYPE = "new_share"

def get_total_shares(user_checkpoint_obj):
    from db import Share
    shares = Share.query.filter_by(user_checkpoint_id=user_checkpoint_obj.id)
    return shares.count()

def get_share(id):
    """
    gets a share record with the supplied id if it already exists, else, None
    """
    from db import Share
    cp = Share.query.filter_by(id=id)
    if cp.count() > 0:
        return cp.first()
    return None

def get_share_w_attr(user_from, user_to, user_checkpoint):
    """
    gets share with the supplied arguments, else, None
    """
    from db import Share
    cp = Share.query.filter_by(user_from_id=user_from.id, user_to_id=user_to.id, user_checkpoint_id=user_checkpoint.id)
    if cp.count() > 0:
        return cp.first()
    return None

def add_share(user_from, user_to, user_checkpoint):
    """
    Adds a share record to the database (if it does not exists)
    """
    share = get_share_w_attr(user_from, user_to, user_checkpoint)
    
    if share is None:
    
        from db import db, Share
        now = datetime.datetime.now()
        
        share = Share()
        share.user_from_id = user_from.id
        share.user_to_id = user_to.id
        share.user_checkpoint_id = user_checkpoint.id
        share.timestamp = now
        
        db.session.add(share)
        db.session.commit()
    
    #add notification
    add_notification(NOTIFICATION_TYPE, user_from, user_to, share.id, user_checkpoint.id)
    
    return share
    
def share(user_from, user_to, user_checkpoint):
    """
    Shares a (User) Checkpoint to a (facebook) user via a Facebook Wall post
    This also creates a (Share) record in the database.  
    """
    checkpoint = user_checkpoint.checkpoint
        
    message = checkpoint.description
    link = "www.google.com"
    name = checkpoint.name
    picture = None
    caption = FACEBOOK_SHARE_CAPTION
    
    #post_on_wall(get_app_access_token(APP_ID, APP_SECRET), user_from.facebook_user.id, message, picture, link, name, caption)
    add_share(user_from, user_to, user_checkpoint)