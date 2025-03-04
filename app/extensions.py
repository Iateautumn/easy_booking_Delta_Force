from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 设置默认登录端点
login_manager.login_message_category = 'info'