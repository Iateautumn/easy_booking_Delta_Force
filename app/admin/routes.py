
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from app.utils.response import success_response, error_response
from app.admin.services import get_reservation_requests, approve_reservation, reject_reservation
from app.admin.services import add_room, modify_room, delete_room, get_all_rooms
from flask_login import current_user
from app.utils.exceptions import BusinessError
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin_permission():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if not current_user.status.value == "Admin":
        return error_response("permission denied", 403)
@admin_bp.route('/reservation/request', methods=['GET'])
def reservation_request():
    try:
        reservation_requests = get_reservation_requests()
        return success_response(reservation_requests)
    except BusinessError as e:
        return error_response(str(e), e.code)

@admin_bp.route('/reservation/approval', methods=['POST'])
def reservation_approval():
    if request.method != 'POST':
        return error_response('Only POST requests are allowed', 400)
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("can not resolve json: " + str(e), 400)
    reservation_id = data['reservation_id']
    try:
        approve_reservation(reservation_id)
        return success_response()
    except BusinessError as e:
        return error_response(str(e), e.code)

@admin_bp.route('/reservation/reject', methods=['POST'])
def reservation_reject():
    if request.method != 'POST':
        return error_response('Only POST requests are allowed', 400)
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("can not resolve json: " + str(e), 400)
    reservation_id = data['reservation_id']
    try:
        reject_reservation(reservation_id)
        return success_response()
    except BusinessError as e:
        return error_response(str(e), e.code)
    
@admin_bp.route('/approval')
def approval():
    return render_template('admin/approval.html')


@admin_bp.route('/management')
def management():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('admin/management.html')

@admin_bp.route('/classroom/add', methods=['POST'])
def add_classroom():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    # user_id = current_user.userId
    user_id = 1
    try:
        add_room(**data)
        return success_response("success reservation")
    except BusinessError as e:
        return error_response(str(e), e.code)
    
@admin_bp.route('/classroom/modify', methods=['POST'])
def modify_classroom():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    # user_id = current_user.userId
    user_id = 1
    try:
        modify_room(**data)
        return success_response("success reservation")
    except BusinessError as e:
        return error_response(str(e), e.code)

@admin_bp.route('/classroom/remove', methods=['POST'])
def delete_classroom():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
    except Exception as e:
        return error_response("bad request: " + str(e), 400)

    user_id = current_user.userId
    try:
        delete_room(**data)
        return success_response("success reservation")
    except BusinessError as e:
        return error_response(str(e), e.code)

@admin_bp.route('/classroom/all')
def all_classroom():
    try:
        return success_response(get_all_rooms())
    except BusinessError as e:
        return error_response(str(e), e.code)