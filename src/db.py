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
    fb_id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    username = db.Column(db.String(255))
    link = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    facebook_info = db.relation("FacebookUser")

class Checkpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.relation("User")
    location = db.relation("Location")
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
    fb_user_from = db.relation("FacebookUser")
    fb_user_to = db.relation("FacebookUser")

class UserCheckpoint(db.Model):
    """
    Stores the catalog of a users' Checkpoint
    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.relation("User")
    checkpoint = db.relation("Checkpoint")
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relation("User")
    comment = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    checkpoint = db.relation("Checkpoint")

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkpoint = db.relation("Checkpoint")
    user = db.relation("User")
    timestamp = db.Column(db.DateTime)
    
class Share(db.Model):
    """
    Stores the Checkpoint shares between users
    """
    id = db.Column(db.Integer, primary_key=True)
    user_from = db.relation("User")
    user_to = db.relation("User")
    checkpoint = db.relation("Checkpoint")
    timestemp = db.Column(db.DateTime)
    share_msg = db.Column(db.String(255))
