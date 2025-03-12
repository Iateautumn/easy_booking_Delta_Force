# models/booking.py

from datetime import datetime
from enum import Enum
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/bookingsystem?charset=utf8'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True # 这一行如果不添加，程序会报警告。
db= SQLAlchemy(app)

class UserStatus(Enum):
    Student = 'Student'
    Teacher = 'Teacher'
    Admin = 'Admin'

class User(db.Model):
    
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
    Classrooms = db.relationship(
        "Classroom", 
        secondary="reservation",
        back_populates="Users"  
    )

    def __init__(self, status, name, email, password_hash, salt):
        self.status = status
        self.name = name
        self.email = email
        self.password = password_hash
        self.salt = salt
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

class Equipment(db.Model):
    __tablename__ = 'equipment'
    equipmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipmentName = db.Column(db.String(50), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)
    Classrooms = db.relationship(
        "Classroom", 
        secondary="classequipment",
        back_populates="Equipments"  # 使用back_populates代替backref
    )

    def __init__(self, equipmentName):
        self.equipmentName = equipmentName
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False


class Classroom(db.Model):

    __tablename__ = 'classroom'
    
    classroomId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroomName = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    constrain= db.Column(db.String(50))
    isRestricted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)
    Users = db.relationship(
        "User",
        secondary="reservation",
        back_populates="Classrooms"  # 保持一致的back_populates
    )
    Equipments = db.relationship(
        "Equipment",
        secondary="classequipment",
        back_populates="Classrooms"  # 保持一致的back_populates
    )

    def __init__(self, classroomName, capacity):
        self.classroomName = classroomName
        self.capacity = capacity
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False


class ClassEquipment(db.Model):
    __tablename__ = 'classequipment'
    classEquipmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroomId = db.Column(db.Integer, db.ForeignKey('classroom.classroomId'), nullable=False)
    equipmentId = db.Column(db.Integer, db.ForeignKey('equipment.equipmentId'), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, classroomId, equipmentId):
        self.classroomId = classroomId
        self.equipmentId = equipmentId
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

class ReservationStatus(Enum):
    
    Reserved = "Reserved"       
    Cancelled = "Cancelled"     
    Finished = "Finished"       
    Rejected = "Rejected"  

 
class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    classroomId = db.Column(db.Integer, db.ForeignKey('classroom.classroomId'), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ReservationStatus), nullable=False, default=ReservationStatus.Reserved)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, userId, classroomId, startTime, endTime):
        self.userId = userId
        self.classroomId = classroomId
        self.startTime = startTime
        self.endTime = endTime
        self.status = ReservationStatus.Reserved
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

    # user = db.relationship('User', back_populates='classrooms')
    # classroom = db.relationship('Classroom', back_populates='users')

# list all reservations
def get_all_reservations():
    list_reservation = Reservation.query.all()
    return list_reservation

# add a new reservation
def add_reservation(userId, classroomId, startTime, endTime):
    new_reservation = Reservation(userId, classroomId, startTime, endTime)
    db.session.add(new_reservation)
    db.session.commit()
    return new_reservation

def get_reservation_by_time(startTime, endTime):
    list_reservation = Reservation.query.filter(Reservation.startTime>=startTime, Reservation.endTime<=endTime).all()
    return list_reservation

def get_reservation_by_id(reservationId):
    reservation = Reservation.query.filter_by(reservationId=reservationId).first()
    return reservation

def get_reservation_by_user_id(userId):
    list_reservation = Reservation.query.filter_by(userId=userId).all()
    return list_reservation

def get_reservation_by_classroom_id(classroomId):
    list_reservation = Reservation.query.filter_by(classroomId=classroomId).all()
    return list_reservation

def get_reservation_by_status(status):
    list_reservation = Reservation.query.filter_by(status=status).all()
    return list_reservation

def delete_reservation(reservationId):
    reservation = Reservation.query.filter_by(reservationId=reservationId).first()
    reservation.isDeleted = True
    db.session.commit()
    return reservation

def update_reservation(reservationId, userId, classroomId, startTime, endTime, status):
    reservation = Reservation.query.filter_by(reservationId=reservationId).first()
    if reservation is None:
        return False
    if userId is not None:
        reservation.userId = userId
    if classroomId is not None:
        reservation.classroomId = classroomId    
    if startTime is not None:
        reservation.startTime = startTime
    if endTime is not None:
        reservation.endTime = endTime
    if status is not None:
        reservation.status = status
    reservation.updatedAt = datetime.now()
    db.session.commit()
    return reservation


@app.route('/')
def index():
    # print((str)(get_all_reservations())) 
    print((str)(add_reservation(1, 1, datetime.now(), datetime.now()))) 
    
    return 'hello world' 

if __name__ == '__main__':
    app.run(debug=True)





