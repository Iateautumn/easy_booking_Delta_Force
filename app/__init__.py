# from flask import Flask, redirect, url_for
# from flask_login import current_user





# app

# def create_app():
#     app = Flask(__name__)

#     @app.route('/')
#     def root_redirect():
#         if current_user.is_authenticated:
#             return redirect(url_for('booking.dashboard'))
#         return redirect(url_for('auth.login'))

#     return app




from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as f:
    data = json.load(f)

database_config = data['database']
database_url = database_config['url']
database_port = database_config['port']
database_username = database_config['username']
database_password = database_config['password']
database_name = database_config['database_name']

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{database_username}:{database_password}@{database_url}:{database_port}/{database_name}?charset=utf8'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from app.auth import models