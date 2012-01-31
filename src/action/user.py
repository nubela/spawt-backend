from facebook.facebook import FacebookApi
from action.facebook_user import addupdate_facebook_user, get_facebook_user
from action.friend_connection import add_friend_connection
from sqlalchemy.orm.util import aliased
from action.demo import create_demo_checkpoints

def save_user(access_token, auth_code):
    """
    updates/saves a user in the database
    and returns the fb_info and the user's saved id about it
    """
    
    #get info
    fb_api = FacebookApi.new(access_token)
    fb_user_info = fb_api.get_info()
    
    #save info into db
    fb_user = addupdate_facebook_user(fb_user_info["id"], fb_user_info["name"], fb_user_info.get("first_name",None), fb_user_info.get("middle_name",None), 
                                fb_user_info.get("last_name",None), fb_user_info.get("gender",None), fb_user_info.get("username",None), fb_user_info["link"])
    user = addupdate_user(fb_user.id, fb_user_info["email"], access_token, auth_code)
    update_social_graph(access_token, fb_user)
    
    return fb_user_info, user

def update_social_graph(access_token, fb_user=None):
    """
    Note: Include fb_user for performance (1 less FB API to call)
    """
    
    #get friends
    fb_api = FacebookApi.new(access_token)
    all_friends = fb_api.get_friends()
    if not fb_user:
        fb_user = get_facebook_user(fb_api.get_info()["id"])
    
    #save friends into db
    for friend in all_friends["data"]:
        fb_friend = addupdate_facebook_user(friend["id"], friend["name"], None, None, None, None, None, None)
        add_friend_connection(fb_user, fb_friend)
        
    return all_friends

def get_user(id):
    from db import User
    user = User.query.filter_by(id=id)
    if user.count() > 0:
        return user.first()
    return None

def get_user_from_email(email):
    from db import User
    user = User.query.filter_by(email=email)
    if user.count() > 0:
        return user.first()
    return None
        
def addupdate_user(fb_user, email, access_token, auth_code):
    
    from db import db, User
    
    user = get_user_from_email(email)
    
    if not user:
        user = User()
    else:
        return user
        
    user.facebook_user_id = fb_user
    user.email = email
    user.auth_code = auth_code
    user.access_token = access_token
        
    db.session.add(user)
    db.session.commit()
    
    create_demo_checkpoints(user)
    
    return user

def get_friends(user_obj, exclude_self=None):
    """
    returns a list of <<User>> objects, if exclude_self is True, it will not consider the current
    user as a friend.
    """
    if exclude_self == None:
        exclude_self = False
    
    from db import db, User, FriendConnection, FacebookUser
    
    FriendFacebookUser, FriendUser = aliased(FacebookUser), aliased(User)
    friends_q = (db.session.query(User, FriendUser).
               join(FacebookUser, FacebookUser.id == User.facebook_user_id).
               join(FriendConnection, FriendConnection.fb_user_from == FacebookUser.id).
               join(FriendFacebookUser, FriendConnection.fb_user_to == FriendFacebookUser.id).
               join(FriendUser, FriendUser.facebook_user_id == FriendFacebookUser.id)
               )
    friends_q = friends_q.filter(User.id == user_obj.id)
    
    friends = [f[1] for f in friends_q.all()]
    if not exclude_self:
        friends += [user_obj]
    
    return friends