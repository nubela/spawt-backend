#===============================================================================
# Checkpoint API Endpoints
#===============================================================================

def new_checkpoint(lat, lang, image):
    """
    (PUT: checkpoint)
    creates a barebone checkpoint (just location and image)
    this checkpoint is not complete yet.
    """
    pass

def add_checkpoint():
    """
    (PUT: interesting_checkpoint)
    user likes a Checkpoint from a user and wants to add it into his catalog;
    adds checkpoint to user's catalog
    """
    pass

def update_checkpoint(checkpoint_id, **kwargs):
    """
    (POST: checkpoint)
    updates a checkpoint with its meta info.
    checkpoint will be complete after
    """
    pass

def new_share(checkpoint_id, user_from, user_to):
    """
    (PUT: checkpoint)
    instantiates a share from a user to his facebook friend (be it a ctrleff user or not)
    """
    pass

def new_like(checkpoint_id, user_from):
    """
    (PUT: like)
    instantiates a like from a user onto a checkpoint
    """
    pass

def new_comment(checkpoint_id, user_from, comment):
    """
    (PUT: comment)
    instantiates a comment from a user onto a checkpoint
    """
    pass

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """
    
    #checkpoint endpoints
    app.add_url_rule('/checkpoint/', 
                     "new_checkpoint", new_checkpoint, methods=['PUT'])
    app.add_url_rule('/checkpoint/', 
                     "update_checkpoint", update_checkpoint, methods=['POST'])
    
    #share endpoints
    app.add_url_rule('/share/', 
                     "new_share", new_share, methods=['PUT'])
    
    #like endpoints
    app.add_url_rule('/like/', 
                     "new_like", new_like, methods=['PUT'])
    
    #comment endpoints
    app.add_url_rule('/comment/', 
                     "new_comment", new_comment, methods=['PUT'])