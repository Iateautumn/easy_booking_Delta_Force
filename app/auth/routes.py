# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from app.auth.services import register_user, login_user
from app.utils.response import success_response, error_response
from app.auth.exceptions import BusinessError
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('booking.dashboard'))
    try:
        data = request.get_json()
    except Exception:
        return render_template('auth/login.html')
    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        try:
            user = login_user(username, password)
        except BusinessError as e:
            return error_response(str(e), e.code)

        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('booking.dashboard'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('booking.dashboard'))

    try:
        data = request.get_json()
    except Exception:
        return render_template('auth/register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            register_user(username, email, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except BusinessError as e:
            return error_response(str(e),e.code)

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))