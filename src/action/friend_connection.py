#===============================================================================
# friend connection action layer
#===============================================================================

def get_friend_connection(fb_user_from, fb_user_to):
    from db import FriendConnection
    friend_connection_a = FriendConnection.query.filter_by(fb_user_from=fb_user_from.id, fb_user_to=fb_user_to.id)
    
    if friend_connection_a.count() > 0: return friend_connection_a
    return None

def add_friend_connection(fb_user_a, fb_user_b, commit=True):
    
    from db import db, FriendConnection
    
    if not get_friend_connection(fb_user_a, fb_user_b):
        
        friend_connection = FriendConnection()
        friend_connection.fb_user_from = fb_user_a.id
        friend_connection.fb_user_to = fb_user_b.id
        
        db.session.add(friend_connection)
        if commit:
            db.session.commit()
        
def sanify_friends(friends):
    friends_lis = [{"user_id": f.id,
                    "facebook_user_id": f.facebook_user_id,
                    "full_name": f.facebook_user.name,
                    } for f in friends]
    return friends_lis