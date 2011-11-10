from ctrleff import get_app
from local_config import SQL_URI
from flaskext.sqlalchemy import SQLAlchemy

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

class Checkpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.String(255), db.ForeignKey('facebook_user.id'))
    description = db.Column(db.String(255))
    price = db.Column(db.Float)
    expiry = db.Column(db.DateTime)
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
    Stores the catalog of a users' Checkpoint
    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    checkpoint = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    checkpoint = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkpoint = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)
    
class Share(db.Model):
    """
    Stores the Checkpoint shares between users
    """
    id = db.Column(db.Integer, primary_key=True)
    user_from = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    checkpoint = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    timestemp = db.Column(db.DateTime)
    share_msg = db.Column(db.String(255))