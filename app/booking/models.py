# models/reservation.py
from app.extensions import db
from datetime import datetime
from enum import Enum
# from app.auth.models import User
# from app.classroom.models import Classroom


class ReservationStatus(Enum):
    
    Reserved = "Reserved"       
    Cancelled = "Cancelled"     
    Finished = "Finished"       
    Rejected = "Rejected"  
    Pending = "Pending"

 
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

    def __init__(self, userId, classroomId, startTime, endTime,status):
        self.userId = userId
        self.classroomId = classroomId
        self.startTime = startTime
        self.endTime = endTime
        self.status = status
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

    # user = db.relationship('User', back_populates='classrooms')
    # classroom = db.relationship('Classroom', back_populates='users')
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    classroom = db.relationship('Classroom', backref=db.backref('reservations', lazy=True))

# list all reservations
def get_all_reservations():
    list_reservation = Reservation.query.filter_by(isDeleted=False).all()
    return list_reservation

# add a new reservation
def add_reservation(userId, classroomId, startTime, endTime, status):
    new_reservation = Reservation(userId, classroomId, startTime, endTime,status)
    db.session.add(new_reservation)
    db.session.commit()
    return new_reservation

def get_reservation_by_filter(userId=None, classroomId=None, startTime=None, endTime=None, status=None):
    query = Reservation.query
    if userId is not None:
        query = query.filter_by(userId=userId)
    if classroomId is not None:
        query = query.filter_by(classroomId=classroomId)
    if startTime is not None:
        query = query.filter(Reservation.startTime>=startTime)
    if endTime is not None:
        query = query.filter(Reservation.endTime<=endTime)
    if status is not None:
        query = query.filter_by(status=status)
    query = query.filter_by(isDeleted=False)
    list_reservation = query.all()
    return list_reservation


def get_reservation_by_time(startTime, endTime):
    list_reservation = Reservation.query.filter(Reservation.startTime>=startTime, Reservation.endTime<=endTime,Reservation.isDeleted == False).all()
    return list_reservation

def get_reservation_by_id(reservationId):
    reservation = Reservation.query.filter_by(reservationId=reservationId,isDeleted=False).first()
    return reservation

def get_reservation_by_user_id(userId):
    list_reservation = Reservation.query.filter_by(userId=userId,isDeleted=False).all()
    return list_reservation

def get_reservation_by_classroom_id(classroomId):
    list_reservation = Reservation.query.filter_by(classroomId=classroomId,isDeleted=False).all()
    return list_reservation

def get_reservation_by_status(status):
    list_reservation = Reservation.query.filter_by(status=status,isDeleted=False).all()
    return list_reservation

def delete_reservation(reservationId):
    reservation = Reservation.query.filter_by(reservationId=reservationId).first()
    reservation.isDeleted = True
    db.session.commit()
    return reservation

def update_reservation(reservationId, userId = None, classroomId = None, startTime = None, endTime = None, status = None):
    reservation = Reservation.query.filter_by(reservationId=reservationId,isDeleted=False).first()
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


def cancel_reservation(reservationId):
    reservation = Reservation.query.filter_by(reservationId=reservationId,isDeleted=False).first()
    if reservation is None:
        return False
    reservation.status = ReservationStatus.Cancelled
    reservation.updatedAt = datetime.now()
    db.session.commit()
    return reservation