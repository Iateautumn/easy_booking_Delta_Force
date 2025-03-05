# models/user.py
from app import db,app
from datetime import datetime
from enum import Enum



# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/bookingsystem?charset=utf8'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# db = SQLAlchemy(app)

class UserStatus(Enum):
    Student = 'Student'
    Teacher = 'Teacher'
    Admin = 'Admin'

class User(db.Model):
    
    __tablename__ = 'User'
    
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(UserStatus), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)  # in db is 0 or 1, 0 represents exist

    def __init__(self, status, name, email, password_hash, salt):
        self.status = status
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.salt = salt


def get_all_users():
    list_usrs = User.query.all()
    # for usr in list_usrs:
    #     print(usr.name, 
    #           usr.email, 
    #           usr.status, 
    #           usr.createdAt, 
    #           usr.updatedAt, 
    #           usr.isDeleted
    #           )
    return list_usrs


def each_user_info(list_usrs):
    result = ''
    for usr in list_usrs:
        result += f'User ID: {usr.userId}\n'
        result += f'Status: {usr.status.value}\n'
        result += f'Name: {usr.name}\n'
        result += f'Email: {usr.email}\n'
        result += f'Password: {usr.password}\n'
        result += f'Salt: {usr.salt}\n'
        result += f'Created At: {usr.createdAt}\n'
        result += f'Updated At: {usr.updatedAt}\n'
        result += f'Is Deleted: {usr.isDeleted}\n'
        result += '--\n'
    return result


@app.route('/user_model')
def index():
    list_usrs = get_all_users()
    return each_user_info(list_usrs)


# if __name__ == '__main__':
    
#     app.run(debug=True)



