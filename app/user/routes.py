from flask import Blueprint, render_template, redirect, url_for, request, send_file
from flask_login import current_user
from app.user.services import own_reservations
from .services import *
from app.utils.response import success_response, error_response
from app.utils.exceptions import BusinessError
import os

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

@user_bp.route('/calendar', methods=['GET', 'POST'])
def output_all_calendar():
    
    user_id = current_user.userId
    if request.method == 'GET':
        reservation_ids = None
    elif request.method == 'POST':
        try:
            data = request.get_json()
            reservation_ids = data.get('reservation_id')
        except Exception as e:
            return error_response("bad request: " + str(e), 400)
    
    try:
        ics_file_path = to_calendar(user_id, reservation_ids=reservation_ids)
        response = send_file(ics_file_path, as_attachment=True, download_name="reservations.ics")
        # TODO: elegantly delete the temp file after sending finished
        # os.remove(ics_file_path)
        return response
    except Exception as e:
        return error_response(str(e), e.code)
        print(e)
        raise NotImplementedError

@user_bp.route('/classroom/issue/report', methods=['POST'])
def issue_report():
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    user_id = current_user.userId
    issue = data.get('issue')

    try:
        report_issue(user_id, issue)
        return success_response("success issue report")
    except BusinessError as e:
        return error_response(str(e), e.code)
