from flask import Flask, redirect, url_for
from flask_login import current_user


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def root_redirect():
        if current_user.is_authenticated:
            return redirect(url_for('booking.dashboard'))
        return redirect(url_for('auth.login'))

    return app