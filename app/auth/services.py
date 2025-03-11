# app/auth/services.py
from werkzeug.security import check_password_hash, generate_password_hash
import app.auth.models as Model
from app.extensions import db

def register_user(username, email, password):
    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

