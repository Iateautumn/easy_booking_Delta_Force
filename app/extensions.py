from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.auth.models import User
    return User.query.get(int(user_id))

def init_db(app):
    # 数据库配置
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

    # 初始化数据库
    db.init_app(app)