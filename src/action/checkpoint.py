"""
Action layer for manipulation of Checkpoints
"""
def get_checkpoint(id):
    """
    Gets the relevant Checkpoint from Database with the given ID
    """
    from db import Checkpoint
    cp = Checkpoint.query.filter_by(id=id)
    if cp.count() > 0:
        return cp.first()
    return None

def add_checkpoint(creator_id, location_id, name, type, image, description=None, price=None, expiry=None):
    """
    Creates a Checkpoint record in the database with the supplied arguments
    """
    
    from db import Checkpoint, db

    checkpoint = Checkpoint()
    checkpoint.creator = creator_id
    checkpoint.location = location_id
    checkpoint.name = name
    checkpoint.description = description
    checkpoint.price = price
    checkpoint.expiry = expiry
    checkpoint.type = type
    checkpoint.image = image
     
    db.session.add(checkpoint)
    db.session.commit() 
    
    return checkpoint