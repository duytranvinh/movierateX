from datetime import datetime
from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import backref


class User(UserMixin, db.Model):
    """
    This class is responsible for storing user's login information.
    All of the attributes for this class are listed below. 
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    settings = db.Column(db.Text, default='')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Post(db.Model):
    """
    This class is responsible for storing user's review information.
    All of the attributes for this class are listed below. 
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(128))
    item_id = db.Column(db.Integer, index=True)
    rating = db.Column(db.Integer)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Posts {}>'.format(self.body)

class Feedback(db.Model):
    """
    This class is responsible for storing user's feedback information.
    All of the attributes for this class are listed below. 
    """
    __tablename__ = "Feedback"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Feedback {}>'.format(self.body)
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
