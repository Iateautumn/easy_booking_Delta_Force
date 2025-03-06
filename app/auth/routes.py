# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app.auth.services import register_user, my_login_user
from app.utils.response import success_response, error_response
from app.utils.exceptions import BusinessError

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
        username = data.get('email')
        password = data.get('password')
        try:
            user = my_login_user(username, password)
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
    except Exception as e:
        return error_response("bad request: " + str(e), 400)
    if request.method == 'POST':
        status = data.get('status')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        try:
            register_user(status, username, email, password)
            return success_response("register successfully")
        except BusinessError as e:
            return error_response(str(e),e.code)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# 测试用例
# @auth_bp.route('/test')
# def test():
#     # print((str)(Services.Model.get_all_users()))
#     # print((str)(Services.Model.get_user_by_id(1).name))
#     # Services.Model.delete_user(1)

#     # Services.Model.add_user("Teacher", "test", "test@test.com", "test", "test")
#     Services.Model.update_user(3, "Teacher", "test", "test2@test.com", "test", "test")
    
#     return "test"