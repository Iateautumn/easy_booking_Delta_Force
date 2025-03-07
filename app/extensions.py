from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.auth.models import User

    return User.query.filter_by(userId=int(user_id)).first()

def init_db(app):
    with open('config.json', 'r') as f:
        data = json.load(f)

    database_config = data['database']
    database_url = database_config['url']
    database_port = database_config['port']
    database_username = database_config['username']
    database_password = database_config['password']
    database_name = database_config['database_name']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{database_username}:{database_password}@{database_url}:{database_port}/{database_name}?charset=utf8'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


    db.init_app(app)