# app/classrooms/routes.py
import asyncio
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_login import current_user, login_user
from app.auth.services import my_login_user
from app.booking.booking_room import bookings
from app.utils.response import error_response, success_response
from app.utils.exceptions import BusinessError

from app.booking.services import new_booking


booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/bookroom', methods=['GET'])
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('user/bookroom.html')

@booking_bp.route('/new', methods=['POST'])
def booking_room():

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    user_id = current_user.userId
    room_id = data['room_id']
    time_period = data['time_period']
    date = data['date']

    try:
        asyncio.run(new_booking(user_id, room_id, time_period, date))
        return success_response("success reservation")
    except BusinessError as e:
        return error_response(e.message, e.code)



