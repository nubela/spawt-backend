def get_facebook_user(id):
    from db import FacebookUser
    return FacebookUser.query.get(id=id)

def addupdate_facebook_user(fb_id, name, first_name, middle_name,
                      last_name, gender, username, link):
    
    from db import db, FacebookUser
    
    fb_user = FacebookUser.query.get(fb_id)
    
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
        db.session.add(fb_user_obj)
    else:
        fb_user_obj = db.session.merge(fb_user)

    db.session.commit()
    
    return fb_user_obj