from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app.user.services import own_reservations
from app.utils.response import success_response, error_response
from app.utils.exceptions import BusinessError

user_bp = Blueprint('user', __name__, url_prefix='/user')
@user_bp.route('/reservation', methods=['GET', 'POST'])
def reservations():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == 'GET':
        user_id = current_user.userId
        try:
            users = own_reservations(user_id)
        except BusinessError as e:
            return error_response(str(e), e.code)
        return success_response(users)

@user_bp.route('/bookroom')
def bookroom():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('user/bookroom.html')

@user_bp.route('/mybookings')
def mybookings():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template("user/mybookings.html")

