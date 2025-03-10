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




class ClassroomType(db.Model):
    __tablename__ = 'classroomType'
    
    typeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typeName = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, typeName, capacity, equipment):
        self.typeName = typeName
        self.capacity = capacity
        self.equipment = equipment
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

def get_all_classroom_types():
    list_classroom_type = ClassroomType.query.all()
    return list_classroom_type

def add_classroom_type(typeName, capacity, equipment):
    new_classroom_type = ClassroomType(typeName, capacity, equipment)
    db.session.add(new_classroom_type)
    db.session.commit()
    return new_classroom_type

def get_classroom_type_by_id(typeId):
    classroom_type = ClassroomType.query.filter_by(typeId=typeId).first()
    return classroom_type

def get_classroom_type_by_name(typeName):
    classroom_type = ClassroomType.query.filter_by(typeName=typeName).first()
    return classroom_type

def delete_classroom_type(typeId):
    classroom_type = ClassroomType.query.filter_by(typeId=typeId).first()
    classroom_type.isDeleted = True
    db.session.commit()
    return classroom_type

def get_classroom_type_by_capacity(capacity):
    list_classroom_type = ClassroomType.query.filter(ClassroomType.capacity>=capacity).all()
    return list_classroom_type

def update_classroom_type(typeId, typeName, capacity, equipment):
    classroom_type = ClassroomType.query.filter_by(typeId=typeId).first()
    if classroom_type is None:
        return False
    if typeName is not None:
        classroom_type.typeName = typeName
    if capacity is not None:
        classroom_type.capacity = capacity
    if equipment is not None:
        classroom_type.equipment = equipment
    classroom_type.updatedAt = datetime.now()
    db.session.commit()
    return classroom_type



class Classroom(db.Model):

    __tablename__ = 'classroom'
    
    classroomId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroomNumber = db.Column(db.String(20), nullable=False)
    building = db.Column(db.String(50), nullable=False)
    typeId = db.Column(db.Integer, db.ForeignKey('classroomType.typeId'), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    classroomType = db.relationship('ClassroomType')
    Users = db.relationship(
        "User",
        secondary="reservation",
        back_populates="Classrooms"  # 保持一致的back_populates
    )

    def __init__(self, classroomNumber, building, typeId):
        self.classroomNumber = classroomNumber
        self.building = building
        self.typeId = typeId
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

def get_all_classeooms():
    list_classroom = Classroom.query.all()
    return list_classroom

def add_classroom(classroomNumber, building, typeId):
    new_classroom = Classroom(classroomNumber, building, typeId)
    db.session.add(new_classroom)
    db.session.commit()
    return new_classroom

def get_classroom_by_id(classroomId):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    return classroom

def get_classroom_by_number(classroomNumber):
    classroom = Classroom.query.filter_by(classroomNumber=classroomNumber).first()
    return classroom
def get_classroom_by_building(building):
    list_classroom = Classroom.query.filter_by(building=building).all()
    return list_classroom

def get_classroom_by_type_id(typeId):
    list_classroom = Classroom.query.filter_by(typeId=typeId).all()
    return list_classroom

def delete_classroom(classroomId):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    classroom.isDeleted = True
    db.session.commit()
    return classroom

def update_classroom(classroomId = None, classroomNumber = None, building = None, typeId = None):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    if classroom is None:
        return False
    if classroomNumber is not None:
        classroom.classroomNumber = classroomNumber
    if building is not None:
        classroom.building = building
    if typeId is not None:
        classroom.typeId = typeId
    classroom.updatedAt = datetime.now()
    db.session.commit()
    return classroom


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
        back_populates="Users"  # 使用back_populates代替backref
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
    # print((str)(get_all_classroom_types()[0].typeName))
    # add_classroom_type("test",100,"test")
    # print((str)(get_classroom_type_by_id(1).typeName))
    # print((str)(get_classroom_type_by_name('Lecture Hall').typeName))
    # print((str)(get_classroom_type_by_capacity(100)))
    # print((str)(update_classroom_type(typeId=1, typeName='test2', capacity=200, equipment='test2')))
    # print((str)(get_all_classeooms()[0].classroomNumber)) 
    # print((str)(add_classroom('101', 'Z', 1))) 
    # print((str)(get_classroom_by_type_id(1)[0].classroomNumber))
    # print((str)(delete_classroom(1).classroomNumber))
    # print((str)(update_classroom(classroomId=1, classroomNumber='102', building='Z', typeId=1)))
    print((str)(get_all_reservations()[0]))

    return 'hello world' 

if __name__ == '__main__':
    app.run(debug=True)





