from ctrleff import get_app
from flaskext.sqlalchemy import SQLAlchemy
from local_config import SQL_URI

app = get_app()
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI
db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

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
    facebook_info = db.Column(db.String(255), db.ForeignKey('facebook_user.id'))
    facebook_user = db.relationship("FacebookUser")
    
    #authentication 
    auth_code = db.Column(db.String(255), nullable=True)
    access_token = db.Column(db.String(255), nullable=True)

class Checkpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.String(255), db.ForeignKey('location.id'))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255), nullable=True)
    #tell_a_friend = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=True)
    expiry = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime)
    type = db.Column(db.String(255))
    image = db.Column(db.String(255))
    
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

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
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
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    to_user = db.relationship("User", primaryjoin="Notification.to_user_id==User.id")
    relevant_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    fresh = db.Column(db.Boolean)  
    