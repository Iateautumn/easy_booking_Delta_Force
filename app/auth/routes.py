# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('booking.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('booking.dashboard'))
    return render_template('auth/register.html')