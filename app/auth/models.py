# models/user.py
from app.extensions import db
from datetime import datetime
from enum import Enum
from flask_login import UserMixin


class UserStatus(Enum):
    Student = 'Student'
    Teacher = 'Teacher'
    Admin = 'Admin'

class User(UserMixin,db.Model):
    
    __tablename__ = 'User'
    
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(UserStatus), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)  # in db is 0 or 1, 0 represents exist

    def __init__(self, status, name, email, password_hash, salt):
        self.status = status
        self.name = name
        self.email = email
        self.password = password_hash
        self.salt = salt
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

# add user
def add_user(status, name, email, password_hash, salt):
    user = User(status, name, email, password_hash, salt)
    db.session.add(user)
    db.session.commit()
    return user

def get_all_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_name(name):
    return User.query.filter_by(name=name).first()

def get_user_by_id(user_id):
    return User.query.filter_by(userId=user_id).first()

def get_user_by_status(status):
    return User.query.filter_by(status=status).all()

def update_user(user_id, status = None, name = None, email = None, password_hash = None, salt = None):
    if user_id is not None:
        user = get_user_by_id(user_id)
    if status is not None:
        user.status = status
    if name is not None:
        user.name = name
    if email is not None:
        if get_user_by_email(email) is None:
            user.email = email
        else:
            return False
    if password_hash is not None:
        user.password_hash = password_hash
    if salt is not None:    
        user.salt = salt
    user.updatedAt = datetime.now()
    db.session.commit()
    return user

def delete_user(user_id):
    user = get_user_by_id(user_id)
    user.isDeleted = True
    db.session.commit()
    return user






