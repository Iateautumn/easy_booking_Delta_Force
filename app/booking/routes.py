# app/classrooms/routes.py
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user
from app.utils.response import error_response, success_response
from app.utils.exceptions import BusinessError

from app.booking.services import new_booking,filter_classrooms
import app.booking.services as Services

classroom_bp = Blueprint('booking', __name__,url_prefix='/booking')

@classroom_bp.route('/new', methods=['POST'])
def list_classrooms():

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    room_id = data['room_id']
    time_period = data['time_period']

    try:
        new_booking(room_id, time_period)
        return success_response("success reservation")
    except BusinessError as e:
        return error_response(str(e), e.code)




