from werkzeug.security import generate_password_hash
from app.auth.models import User, add_user, get_user_by_email
from app.utils.exceptions import BusinessError
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def generate_password_hash(password, salt=None):
    if salt is None:
        salt = os.urandom(4)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    password_hash = kdf.derive(password.encode())
    return password_hash.hex(), salt.hex()


def register_user(status, username, email, password):
    password_hash, salt = generate_password_hash(password)

    try:
        user = add_user(status, username, email, password_hash, salt)
    except Exception as e:
        raise BusinessError('Failed to register user: ' + str(e), 409)

    return user


def my_login_user(username, password):
    try:
        user = get_user_by_email(username)
    except Exception as e:
        raise BusinessError('Failed to login user: ' + str(e), 500)
    if not user:
        raise BusinessError('Invalid username or password', 401)

    salt = bytes.fromhex(user.salt)
    password_hash = user.password

    hashed_password, salt = generate_password_hash(password, salt=salt)

    if password_hash == hashed_password:
        return user
    else:
        raise BusinessError('Invalid username or password', 401)

