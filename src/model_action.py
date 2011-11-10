def get_facebook_user(id):
    return FacebookUser.query.get(id=id) #@UndefinedVariable

def addupdate_facebook_user(fb_id, name, first_name, middle_name,
                      last_name, gender, username, link):
    
    from db import db, FacebookUser
    
    fb_user = FacebookUser.query.get(fb_id) #@UndefinedVariable
    
    fb_user_obj = FacebookUser()
    fb_user_obj.id = fb_id
    fb_user_obj.name = name
    fb_user_obj.first_name = first_name
    fb_user_obj.middle_name = middle_name
    fb_user_obj.last_name = last_name
    fb_user_obj.gender = gender
    fb_user_obj.username = username
    fb_user_obj.link = link
    
    if not fb_user:
        db.session.add(fb_user_obj) #@UndefinedVariable
    else:
        fb_user_obj = db.session.merge(fb_user) #@UndefinedVariable

    db.session.commit() #@UndefinedVariable
    
    return fb_user_obj

def get_user(email):
    from db import User
    user = User.query.filter_by(email=email) #@UndefinedVariable
    if user.count() > 0:
        return user.first()
    return None
        
def add_user(fb_user, email):
    
    from db import db, User
    
    user = get_user(email) #@UndefinedVariable
    
    if not user:
        user = User()
        user.facebook_info = fb_user
        user.email = email
        
        db.session.add(user) #@UndefinedVariable
        db.session.commit() #@UndefinedVariable
    
    return user

def get_friend_connection(fb_user_a, fb_user_b):
    from db import FriendConnection
    friend_connection_a = FriendConnection.query.filter_by(fb_user_from=fb_user_a.id, fb_user_to=fb_user_b.id) #@UndefinedVariable
    friend_connection_b = FriendConnection.query.filter_by(fb_user_to=fb_user_a.id, fb_user_from=fb_user_b.id) #@UndefinedVariable
    
    if friend_connection_a.count() > 0: return friend_connection_a
    elif friend_connection_b.count() > 0: return friend_connection_b
    return None

def add_friend_connection(fb_user_a, fb_user_b):
    
    from db import db, FriendConnection
    
    if not get_friend_connection(fb_user_a, fb_user_b):
        
        friend_connection = FriendConnection()
        friend_connection.fb_user_from = fb_user_a.id
        friend_connection.fb_user_to = fb_user_b.id
        
        db.session.add(friend_connection) #@UndefinedVariable
        db.session.commit() #@UndefinedVariable