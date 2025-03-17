# app/auth/routes.py

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app.auth.services import register_user, my_login_user
from app.utils.response import success_response, error_response
from app.utils.exceptions import BusinessError


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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
            return error_response(str(e), e.code)

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
            return error_response(str(e),e.code)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


