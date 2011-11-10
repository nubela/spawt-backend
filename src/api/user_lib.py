#===============================================================================
# library of methods relevant to user's api'
#===============================================================================
from facebook.facebook import FacebookApi
from model_action import addupdate_facebook_user, add_user, addupdate_facebook_user,\
    get_facebook_user, add_friend_connection

def save_user(access_token):
    """
    updates/saves a user in the database
    and returns information about it
    """
    
    #get info
    fb_api = FacebookApi(access_token)
    user_info = fb_api.get_info()
    
    #save info into db
    fb_user = addupdate_facebook_user(user_info["id"], user_info["name"], user_info.get("first_name",None), user_info.get("middle_name",None), 
                                user_info.get("last_name",None), user_info.get("gender",None), user_info.get("username",None), user_info["link"])
    user = add_user(fb_user.id, user_info["email"])
    update_social_graph(access_token, fb_user)
    
    return user_info

def update_social_graph(access_token, fb_user=None):
    
    #get friends
    fb_api = FacebookApi(access_token)
    all_friends = fb_api.get_friends()
    if not fb_user:
        fb_user = get_facebook_user(fb_api.get_info()["id"])
    
    #save friends into db
    for friend in all_friends["data"]:
        fb_friend = addupdate_facebook_user(friend["id"], friend["name"], None, None, None, None, None, None)
        add_friend_connection(fb_user, fb_friend)
        
    return all_friends