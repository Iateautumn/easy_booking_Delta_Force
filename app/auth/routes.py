# app/auth/routes.py

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from .services import *
from app.utils.response import success_response, error_response
from app.utils.exceptions import BusinessError


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
email_auth_bp = Blueprint('email_auth', __name__, url_prefix='/email')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.bookroom'))

    try:
        data = request.get_json()
    except Exception:
        return render_template('auth/login.html')
    if request.method == 'POST':
        username = data.get('email')
        password = data.get('password')
        try:
            user = my_login_user(username, password)
        except BusinessError as e:
            return error_response(e.message, e.code)

        login_user(user)
        next_page = request.args.get('next')
        return redirect(url_for('user.bookroom')) if user.status.value != "Admin" else redirect(url_for('admin.bookroom'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('booking.dashboard'))
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)
    if request.method == 'POST':
        status = data.get('status')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        try:
            register_user(status, username, email, password)
            return success_response("register successfully")
        except BusinessError as e:
            return error_response(e.message, e.code)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@email_auth_bp.route('/code/login', methods=['POST'])
def code_login():
    if current_user.is_authenticated:
        return redirect(url_for('user.bookroom'))

    try:
        data = request.get_json()
    except Exception:
        return render_template('auth/login.html')

    try:
        user = verify_code(**data)
        login_user(user)
        next_page = request.args.get('next')
        return redirect(url_for('user.bookroom')) if user.status.value != "Admin" else redirect(url_for('admin.bookroom'))
    except BusinessError as e:
        return error_response(e.message, e.code)

@email_auth_bp.route('/code/send', methods=['POST'])
def send_email_code():
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)
    try:
        asyncio.run(send_email_async(**data))
        return success_response("send email successfully")
    except BusinessError as e:
        return error_response(e.message, e.code)

@email_auth_bp.route('/registration-code/send', methods=['POST'])
def signup_send_email_code():
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)
    try:
        asyncio.run(send_email_async(**data, type="register"))
        return success_response("send email successfully")
    except BusinessError as e:
        return error_response(e.message, e.code)
    
@email_auth_bp.route('/registration-code/register', methods=['POST'])
def code_signup():
    if current_user.is_authenticated:
        return redirect(url_for('booking.dashboard'))
    try:
        data = request.get_json()
    except Exception as e: 
        return error_response("bad request: " + str(e), 400)
    try:
        signup_verify_code(**data)
        return success_response("register successfully")
    except BusinessError as e:
        return error_response(e.message, e.code)
