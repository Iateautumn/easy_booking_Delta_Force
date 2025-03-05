from flask import Flask, redirect, url_for, request  # 导入 request
from flask_login import current_user, LoginManager    # 导入 LoginManager
from app.auth.routes import auth_bp
from app.extensions import login_manager, db
import json

def create_app():
    app = Flask(__name__)


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

    app.config['SECRET_KEY'] = 'your-secret-key-here'  # 设置密钥

    # 初始化 Flask-Login
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'  # 指定登录视图端点
    db.init_app(app)
    login_manager.init_app(app)  # 初始化 Flask-Login
    login_manager.login_view = 'auth.login'  # 设置登录端点
    # 先注册蓝图
    app.register_blueprint(auth_bp)

    # 根路由
    @app.route('/')
    def root_redirect():
        if current_user.is_authenticated:
            return redirect(url_for('booking.dashboard'))
        return redirect(url_for('auth.login'))

    # 全局认证检查钩子
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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)