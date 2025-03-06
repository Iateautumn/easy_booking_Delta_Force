# app/classrooms/routes.py
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_login import current_user
from app.booking.booking_room import bookings
from app.utils.response import error_response, success_response
from app.utils.exceptions import BusinessError

from app.booking.services import new_booking,filter_classrooms


booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('/booking/dashboard.html')

@booking_bp.route('/new', methods=['POST'])
def list_classrooms():

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    user_id = current_user.id
    room_id = data['room_id']
    time_period = data['time_period']
    date = data['date']

    try:
        new_booking(user_id, room_id, time_period, date)
        return success_response("success reservation")
    except BusinessError as e:
        return error_response(str(e), e.code)




