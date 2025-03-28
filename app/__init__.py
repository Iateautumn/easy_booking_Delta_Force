from flask import Flask, redirect, url_for, request
from flask_login import current_user

from app.user.routes import user_bp

from app.admin.routes import admin_bp

from app.auth.routes import auth_bp, email_auth_bp
from app.booking.routes import booking_bp
from app.classroom.routes import classroom_bp
from app.extensions import db, login_manager, init_db

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.config['SECRET_KEY'] = 'your-secret-key-here'

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(classroom_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(email_auth_bp)

    @app.route('/')
    def root_redirect():
        if current_user.is_authenticated:
            if current_user.status.value == 'Admin':
                return redirect(url_for('admin.bookroom'))
            else:
                return redirect(url_for('user.bookroom'))
        return redirect(url_for('auth.login'))

    # @app.before_request
    # def check_authentication():
    #
    #     if request.path.startswith('/static'):
    #         return
    #     if request.endpoint in ['auth.login', 'auth.register']:
    #         return
    #
    #     if not current_user.is_authenticated:
    #         return redirect(url_for('auth.login', next=request.full_path))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
