from ctrleff import get_app
from flaskext.sqlalchemy import SQLAlchemy
from local_config import SQL_URI
from sqlalchemy.dialects.mysql.base import DOUBLE
from rest_client.rest import serialize_json_datetime
from action.serve import get_checkpoint_img_url

app = get_app()
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI
db = SQLAlchemy(app)

class FacebookUser(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    first_name = db.Column(db.String(255), nullable=True)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(255), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    facebook_user_id = db.Column(db.String(255), db.ForeignKey('facebook_user.id'))
    facebook_user = db.relationship("FacebookUser")
    
    #authentication 
    auth_code = db.Column(db.String(255), nullable=True)
    access_token = db.Column(db.String(255), nullable=True)

class Checkpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=True)
    expiry = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime)
    type = db.Column(db.String(255))
    image = db.Column(db.String(255))
    longitude = db.Column(DOUBLE)
    latitude = db.Column(DOUBLE)
    
    @property
    def serialize(self):
        """
        Return this object data into an easily serializable form (For JSON)
        """
        from action.like import get_total_likes_checkpoint
        from action.comment import get_checkpoint_comments
        from action.user import get_user
        
        return {
                "id": self.id,
                "creator": self.creator,
                "creator_name": get_user(self.creator).facebook_user.name,
                "name": self.name,
                "description": self.description,
                "price": self.price,
                "expiry": serialize_json_datetime(self.expiry),
                "date_created": serialize_json_datetime(self.date_created),
                "type": self.type,
                "image": self.image,
                "image_url": get_checkpoint_img_url(self),
                "longitude": self.longitude,
                "latitude": self.latitude,
                
                "total_likes": get_total_likes_checkpoint(self),
                "total_comments": get_checkpoint_comments(self).count(),
                }
    
class FriendConnection(db.Model):
    """
    Describes a two-way connection between 2 friends on Facebook 
    """
    id = db.Column(db.Integer, primary_key=True)
    fb_user_from = db.Column(db.String(255), db.ForeignKey('facebook_user.id'))
    fb_user_to = db.Column(db.String(255), db.ForeignKey('facebook_user.id'))

class UserCheckpoint(db.Model):
    """
    UserCheckpoints provides a relationship between a user and its catalog of Checkpoints.
    A record of a UserCheckpoint linking the user to a Checkpoint demonstrates that
    the user has the respective Checkpoint in its catalog of checkpoints.
    
    This entirely represents the Checkpoint for that user, meaning that it could override
    info from the Checkpoint by means of <<UserCheckpointOptions>>.
    
    Should another user inherit this 'localised' version of UserCheckpoint, it would inherit
    the <<Checkpoint>> reference, as well all copies of <<UserCheckpointOptions>> that this
    record is related to. The new <<UserCheckpoint>> reference is then independent.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    checkpoint = db.relationship("Checkpoint")
    date_added = db.Column(db.DateTime) 
    
    @property
    def serialize(self):
        """
        Return this object data into an easily serializable form (For JSON)
        """
        return {
                "id": self.id,
                "user_id": self.user_id,
                "user_name": self.user.facebook_user.name,
                "checkpoint": self.checkpoint.serialize,
                }
    
class UserCheckpointOptions(db.Model):
    """
    Stores the meta info of a <<UserCheckpoint>>
    """
    
    id = db.Column(db.Integer, primary_key=True)
    user_checkpoint_id = db.Column(db.Integer, db.ForeignKey('user_checkpoint.id'))
    user_checkpoint = db.relationship("UserCheckpoint")
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    comment = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    checkpoint = db.relationship("Checkpoint")
    
    @property
    def serialize(self):
        """
        Return this object data into an easily serializable form (For JSON)
        """
        return {"id": self.id,
                "user_id": self.user_id,
                "comment": self.comment,
                "timestamp": serialize_json_datetime(self.timestamp),
                "checkpoint_id": self.checkpoint_id,
                "facebook_profile_pic_url": "https://graph.facebook.com/%s/picture" % self.user.facebook_user.id,
                "name": self.user.facebook_user.name,
                }

class CheckpointLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkpoint_id = db.Column(db.Integer, db    .ForeignKey('checkpoint.id'))
    checkpoint = db.relationship("Checkpoint")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    timestamp = db.Column(db.DateTime)
    
class Share(db.Model):
    """
    Stores the Checkpoint shares between users
    """
    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_from = db.relationship("User", primaryjoin="Share.user_from_id==User.id")
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_to = db.relationship("User", primaryjoin="Share.user_to_id==User.id")
    user_checkpoint_id = db.Column(db.Integer, db.ForeignKey('user_checkpoint.id'))
    user_checkpoint = db.relationship("UserCheckpoint")
    timestamp = db.Column(db.DateTime)
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    from_user = db.relationship("User", primaryjoin="Notification.from_user_id==User.id") 
    affected_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    affected_user = db.relationship("User", primaryjoin="Notification.affected_user_id==User.id")
    relevant_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime)
    fresh = db.Column(db.Boolean)
    
    @property
    def serialize(self):
        """
        Return this object data into an easily serializable form (For JSON)
        """
        return {
                "id": self.id,
                "type": self.type,
                "relevant_id": self.relevant_id,
                "description": self.description,
                "timestamp": self.timestamp.isoformat(),
                "fresh": self.fresh
                }