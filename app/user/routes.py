from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app.user.services import own_reservations
from .services import own_reservations, modify_reservation, cancel_my_reservation
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



@user_bp.route('/reservation/modify', methods=['POST'])
def reservation_modify():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)
    
    user_id = current_user.userId
    reservation_id = data['reservation_id']
    date = data['date']
    time_period = data['time_period']

    try:
        modify_reservation(
            reservationId=reservation_id,
            userId=user_id,
            date=date,
            timePeriod=time_period
        )
        return success_response("success modified")
    except BusinessError as e:
        return error_response(str(e), e.code)
    

@user_bp.route('/reservation/cancel', methods=['POST'])
def reservation_cancel():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)
    
    user_id = current_user.userId
    reservation_id = data['reservation_id']

    try:
        cancel_my_reservation(
            reservationId=reservation_id,
            userId=user_id
        )
        return success_response("success cancel")
    except BusinessError as e:
        return error_response(str(e), e.code)
