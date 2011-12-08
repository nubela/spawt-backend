def get_friend_connection(fb_user_a, fb_user_b):
    from db import FriendConnection
    friend_connection_a = FriendConnection.query.filter_by(fb_user_from=fb_user_a.id, fb_user_to=fb_user_b.id)
    friend_connection_b = FriendConnection.query.filter_by(fb_user_to=fb_user_a.id, fb_user_from=fb_user_b.id)
    
    if friend_connection_a.count() > 0: return friend_connection_a
    elif friend_connection_b.count() > 0: return friend_connection_b
    return None

def add_friend_connection(fb_user_a, fb_user_b):
    
    from db import db, FriendConnection
    
    if not get_friend_connection(fb_user_a, fb_user_b):
        
        friend_connection = FriendConnection()
        friend_connection.fb_user_from = fb_user_a.id
        friend_connection.fb_user_to = fb_user_b.id
        
        db.session.add(friend_connection)
        db.session.commit()