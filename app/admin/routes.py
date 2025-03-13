# admin/routes.py

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app.utils.exceptions import BusinessError


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/management', methods=['GET'])
def login():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('admin/management.html')
