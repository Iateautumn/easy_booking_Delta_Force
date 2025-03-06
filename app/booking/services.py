# app/bookings/services.py
from datetime import datetime
from sqlalchemy import and_
from werkzeug.http import parse_age
from models import add_reservation

from app.extensions import db
from app.booking.models import Reservation as Booking
import app.booking.models as Models


class ConflictError(Exception):
    pass


class PermissionError(Exception):
    pass


def new_booking(user_id, classroom_id, start_time, end_time):

    conflict = Booking.query.filter(
        (Booking.classroom_id == classroom_id) &
        ((Booking.start_time < end_time) &
         (Booking.end_time > start_time))
    ).first()

    if conflict:
        raise ConflictError("该时间段已被预约")

    today = datetime.utcnow().date()
    today_bookings = Booking.query.filter(
        (Booking.user_id == user_id) &
        (Booking.start_time >= today)
    ).count()

    if today_bookings >= 3:
        raise PermissionError("超出每日预约限制")

    booking = Booking(
        user_id=user_id,
        classroom_id=classroom_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(booking)
    db.session.commit()
    return booking

def filter_classrooms(capacity_range, equipments, days):
    pass