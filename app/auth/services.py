# app/auth/services.py
from werkzeug.security import check_password_hash, generate_password_hash
import app.auth.models as Model
from app.auth.models import get_user_by_email, add_user, User, UserStatus
from app.extensions import db

def register_user(status, username, email, password):
    password_hash = generate_password_hash(password)
    status = UserStatus.Student if status == "Student" else UserStatus.Teacher
    user = add_user(status, username, email, password_hash, "asdf")
    return user

def my_login_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user.password, password):
        return user
    return None

