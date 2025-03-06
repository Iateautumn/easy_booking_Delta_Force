# app/bookings/services.py
from datetime import datetime
from lib2to3.fixer_util import touch_import

from sqlalchemy import and_
from werkzeug.http import parse_age
from models import add_reservation
from datetime import datetime, timedelta
from app.extensions import db
from app.booking.models import Reservation as Booking
import app.booking.models as Models

time_slot_map = {
    0: {'start': '08:00:00', 'end': '08:45:00'},
    1: {'start': '08:45:00', 'end': '09:40:00'},
    2: {'start': '10:00:00', 'end': '10:45:00'},
    3: {'start': '10:55:00', 'end': '11:40:00'},
    4: {'start': '14:00:00', 'end': '14:45:00'},
    5: {'start': '14:55:00', 'end': '15:40:00'},
    6: {'start': '16:00:00', 'end': '16:45:00'},
    7: {'start': '16:55:00', 'end': '17:40:00'},
    8: {'start': '19:00:00', 'end': '19:45:00'},
    9: {'start': '19:55:00', 'end': '20:40:00'},
}


def add_time(date_str, time_str):

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    time_delta = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)

    combined_date = date_obj + time_delta

    return combined_date

class ConflictError(Exception):
    pass


class PermissionError(Exception):
    pass


def new_booking(user_id, classroom_id, time_period, date):
    start_time = add_time(date, time_slot_map[time_period]['start'])
    end_time = add_time(date, time_slot_map[time_period]['end'])

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