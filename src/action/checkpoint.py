"""
Action layer for manipulation of Checkpoints
"""
from sqlalchemy.sql.expression import and_
from util.util import exp
from util.geo import proximity_sort
from collections import namedtuple
import datetime
import simplejson

CHECKPOINT_TYPES = ("food", "shop", "play")

def get_checkpoint(id):
    """
    Gets the relevant Checkpoint from Database with the given ID
    """
    from db import Checkpoint
    cp = Checkpoint.query.filter_by(id=id)
    if cp.count() > 0:
        return cp.first()
    return None

def add_checkpoint(creator_id, name, type, image, longitude, latitude, description=None, price=None, expiry=None, demo=None, img_location=None, opts=None):
    """
    Creates a Checkpoint record in the database with the supplied arguments
    """
    if demo is None:
        demo = False
    
    from db import Checkpoint, db

    checkpoint = Checkpoint()
    checkpoint.creator = creator_id
    checkpoint.longitude = longitude
    checkpoint.latitude = latitude
    checkpoint.name = name
    checkpoint.description = description
    checkpoint.price = price
    checkpoint.expiry = expiry
    checkpoint.date_created = datetime.datetime.now()
    checkpoint.type = type
    checkpoint.image = image
    checkpoint.demo = demo
    checkpoint.img_location = img_location
    if not opts is None: 
        checkpoint.options = simplejson.dumps(opts)
     
    db.session.add(checkpoint)
    db.session.commit() 
    
    return checkpoint