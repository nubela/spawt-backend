def add_checkpoint_to_catalog():
    """
    (POST: user_checkpoint)
    user likes a Checkpoint from a user and wants to add it into his catalog;
    adds checkpoint to user's catalog
    """
    
    #req vars
    pass

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/catalog/', 
                     "add_checkpoint_to_catalog", add_checkpoint_to_catalog, methods=['POST'])