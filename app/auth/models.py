# models/user.py
from app.extensions import db
from datetime import datetime
from enum import Enum
from flask_login import UserMixin
# from app.classroom.models import Classroom, ClassroomType
# from app.booking.models import Reservation

class UserStatus(Enum):
    Student = 'Student'
    Teacher = 'Teacher'
    Admin = 'Admin'

class User(UserMixin,db.Model):
    
    __tablename__ = 'user'
    
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(UserStatus), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)  # in db is 0 or 1, 0 represents exist
    # Classrooms = db.relationship(
    #     "Classroom", 
    #     secondary="reservation",
    #     back_populates="Users"  # 使用back_populates代替backref
    # )
    def get_id(self):
        return self.userId

    def __init__(self, status, name, email, password_hash, salt):
        self.status = status
        self.name = name
        self.email = email
        self.password = password_hash
        self.salt = salt
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False
    
    @property
    def classrooms(self):
        from app.classroom.models import Classroom
        from app.booking.models import Reservation
        return Classroom.query.join(Reservation).filter(Reservation.userId == self.userId).all()


# add user
def add_user(status, name, email, password_hash, salt):
    user = User(status, name, email, password_hash, salt)
    db.session.add(user)
    db.session.commit()
    return user

def get_all_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_name(name):
    return User.query.filter_by(name=name).first()

def get_user_by_id(user_id):
    return User.query.filter_by(userId=user_id).first()

def get_user_by_status(status):
    return User.query.filter_by(status=status).all()

def update_user(user_id, status = None, name = None, email = None, password_hash = None, salt = None):
    if user_id is not None:
        user = get_user_by_id(user_id)
    if status is not None:
        user.status = status
    if name is not None:
        user.name = name
    if email is not None:
        if get_user_by_email(email) is None:
            user.email = email
        else:
            return False
    if password_hash is not None:
        user.password_hash = password_hash
    if salt is not None:    
        user.salt = salt
    user.updatedAt = datetime.now()
    db.session.commit()
    return user

def delete_user(user_id):
    user = get_user_by_id(user_id)
    user.isDeleted = True
    db.session.commit()
    return user

def get_users_by_filter(user_id, status = None, name = None, email = None):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    quary = User.query
    if status is not None:
        quary = quary.filter(status=status)
    if name is not None:
        quary = quary.filter(name=name)
    if email is not None:
        quary = quary.filter(email=email)
    return quary.all()

class IssueReport(db.Model):
    __tablename__ = 'issuereport'
    reportId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    
    description = db.Column(db.String(255), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    isBanned = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)
    User = db.relationship('User', backref=db.backref('issue_reports', lazy=True))

    def __init__(self, userId,  description, startTime, endTime):
        self.userId = userId
        
        self.startTime = startTime
        self.endTime = endTime
        self.description = description
        self.isBanned = False
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False



def get_issue_report_by_filter(userId=None, startTime=None, endTime=None, isBanned=None):
    query = IssueReport.query
    if userId is not None:
        query = query.filter_by(userId=userId)
    
    if startTime is not None:
        query = query.filter(IssueReport.startTime>=startTime)
    if endTime is not None:
        query = query.filter(IssueReport.endTime<=endTime)
    if isBanned is not None:
        query = query.filter_by(isBanned=isBanned)
    list_issue_report = query.all()
    return list_issue_report

def get_issue_report_by_id(reportId):
    issue_report = IssueReport.query.filter_by(reportId=reportId).first()
    return issue_report

def get_issue_report_by_user_id(userId):
    list_issue_report = IssueReport.query.filter_by(userId=userId).all()
    return list_issue_report


def delete_issue_report(reportId):
    issue_report = IssueReport.query.filter_by(reportId=reportId).first()
    issue_report.isDeleted = True
    db.session.commit()
    return issue_report

def update_issue_report(reportId, userId = None,decription = None, startTime = None, endTime = None, isBanned = None):
    issue_report = IssueReport.query.filter_by(reportId=reportId).first()
    if issue_report is None:
        return False
    if userId is not None:
        issue_report.userId = userId
    
    if decription is not None:
        issue_report.decription = decription
    if startTime is not None:
        issue_report.startTime = startTime
    if endTime is not None:
        issue_report.endTime = endTime
    if isBanned is not None:
        issue_report.isBanned = isBanned
    issue_report.updatedAt = datetime.now()
    db.session.commit()
    return issue_report 

def add_issue_report(userId, description, startTime, endTime):
    issue_report = IssueReport(userId, description, startTime, endTime)
    db.session.add(issue_report)
    db.session.commit()
    return issue_report   
    






