#===============================================================================
# UserCheckpoint action layer 
#===============================================================================

def get_user_checkpoint(id):
    """
    gets UserCheckpoint record by id
    """
    from db import UserCheckpoint, db
    cp = UserCheckpoint.query.filter_by(id=id)
    if cp.count() > 0:
        return cp.first()
    return None

def get_user_checkpoint_attr(user_obj, checkpoint_obj):
    """
    gets UserCheckpoint record given supplied args
    """
    from db import UserCheckpoint, db
    cp = UserCheckpoint.query.filter_by(user_id = user_obj.id, checkpoint_id = checkpoint_obj.id)
    if cp.count() > 0:
        return cp.first()
    return None

def add_checkpoint_to_user(user_obj, checkpoint_obj):
    """
    Adds a record to the db table to reflect an addition of an NEW Checkpoint 
    to a user's repertoir of Checkpoints
    """
    ucp = get_user_checkpoint_attr(user_obj, checkpoint_obj)
    if not ucp is None:
        return ucp
        
    from db import UserCheckpoint, db
    
    user_checkpoint = UserCheckpoint()
    user_checkpoint.user_id = user_obj.id
    user_checkpoint.checkpoint_id = checkpoint_obj.id
    
    db.session.add(user_checkpoint)
    db.session.commit()
    
    return user_checkpoint
    
def add_existing_checkpoint_to_user(user_obj, user_checkpoint_obj):
    """
    Duplicates a record of an instance of <<UserCheckpoint>> and gives it to
    the provided <<User>>.
    
    Also recursively duplicates corresponding <<UserCheckpointOptions>> and gives it to the
    duplicated instance of <<UserCheckpoint>>
    """
    
    ucp = get_user_checkpoint_attr(user_obj, user_checkpoint_obj.checkpoint)
    if not ucp is None:
        return ucp
    
    from db import UserCheckpoint, UserCheckpointOptions, db
    
    #duplicate UserCheckpoint
    duplicated_ucp = UserCheckpoint()
    duplicated_ucp.user_id = user_obj.id
    duplicated_ucp.checkpoint_id = user_checkpoint_obj.checkpoint_id
    db.session.add(duplicated_ucp)
    
    #duplicate UserCheckpointOptions
    options = UserCheckpointOptions.query.filter_by(user_checkpoint_id=user_checkpoint_obj.id)
    for opt in options:
        duplicated_opt = UserCheckpointOptions()
        duplicated_opt.user_checkpoint_id = duplicated_ucp.id
        duplicated_opt.name = opt.name
        duplicated_opt.value = opt.value
        db.session.add(duplicated_opt)
        
    db.session.commit()
    
    return duplicated_ucp

def checkpoints_by_proximity(user, location_coord, max_friends_cp=50, max_anon_cp=50):
    """
    return nearby checkpoint objects from friends and anonymous users sorted by proximity 
    """
    from db import Checkpoint, db
    longitude = location_coord[1]
    latitude = location_coord[0]
    
    #get nearby friends checkpoints
    friend_cp = []
    exp_gen = exp()
    exp_no = exp_gen.next()
    while len(friend_cp) < max_friends_cp:
        coord_conditions = and_(Checkpoint.longitude <= longitude + exp_no,
                                Checkpoint.longitude >= longitude - exp_no,
                                Checkpoint.latitude <= latitude + exp_no,
                                Checkpoint.latitude >= latitude - exp_no,
                                )
        friend_cp = Checkpoint.query.filter(coord_conditions).all()
        exp_no = exp_gen.next()
    objects = _checkpoints_to_location_namedtuples(friend_cp) 
    sorted_friend_cp = proximity_sort(location_coord, objects, max_friends_cp)
    
    #get nearby anon checkpoints
    anon_cp = []
    exp_gen = exp()
    exp_no = exp_gen.next()
    
    
def _checkpoints_to_location_namedtuples(lis_of_cp):
    Obj = namedtuple("Obj", ("location", "checkpoint"))
    lis = []
    for cp in lis_of_cp:
        lis += [Obj((cp.latitude, cp.longitude), cp)]
    return lis