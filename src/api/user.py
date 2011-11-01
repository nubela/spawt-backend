def user_login(fb_code):
    """
    (PUT: user)
    Method to handle when a user authenticates (from Facebook), be it a new user, or recurring user
    """
    pass

def register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    app.add_url_rule('/user/', 
                     "user_login", user_login, methods=['PUT'])
