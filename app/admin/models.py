# admin/models.py
from app.extensions import db
from datetime import datetime
from enum import Enum

class ReservationStatus(Enum):
    
    Reserved = "Reserved"       
    Cancelled = "Cancelled"     
    Finisher = "Finished"       
    Rejected = "Rejected"       
           

class Reservation(db.Model):
    
    __tablename__ = 'reservation'
    
    reservationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    classroomId = db.Column(db.Integer, db.ForeignKey('classroom.classroomId'), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ReservationStatus), nullable=False, default=ReservationStatus.PENDING)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    user = db.relationship('User')
    classroom = db.relationship('Classroom')

