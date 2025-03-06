# app/auth/services.py
from werkzeug.security import generate_password_hash
from app.auth.models import User, add_user
from app.utils.exceptions import BusinessError
from flask import current_app
import os
import hashlib

def generate_password_hash(password, salt=None):

    if salt is None:
        salt = os.urandom(32).hex()

    password_with_salt = password + salt

    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
    return hashed_password, salt

def register_user(status, username, email, password):

    password_hash, salt = generate_password_hash(password)

    try:
        user = add_user(status, username, email, password_hash, salt)
    except Exception as e:
        raise BusinessError('Failed to register user', 500)

    return user

def login_user(username, password):

    user = User.query.filter_by(username=username).first()

    if not user:
        raise BusinessError('Invalid username or password', 401)

    salt = user.salt
    password_hash = user.password_hash

    hashed_password = current_app.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        bytes.fromhex(salt),
        100000
    )

    hashed_password_hex = hashed_password.hex()

    if password_hash == hashed_password_hex:
        return user
    else:
        raise BusinessError('Invalid username or password', 401)