from flask import Flask, redirect, url_for
from flask_login import current_user


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def root_redirect():
        if current_user.is_authenticated:
            return redirect(url_for('booking.dashboard'))
        return redirect(url_for('auth.login'))

    @app.before_request
    def check_authentication():
        # 排除静态文件和认证相关路由
        if request.path.startswith('/static'):
            return
        if request.endpoint in ['auth.login', 'auth.register']:
            return

        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.full_path))

    return app