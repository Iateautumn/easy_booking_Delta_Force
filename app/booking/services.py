# app/bookings/services.py
from datetime import datetime
from app.utils.exceptions import BusinessError
from sqlalchemy import and_
from werkzeug.http import parse_age
from app.booking.models import add_reservation, get_reservation_by_time, ReservationStatus
from app.utils.datetime_utils import time_slot_map, add_time, slot_time_map, get_current_date
from app.extensions import db
from app.classroom.models import get_classroom_by_id

def get_certain_reservation(classrooom_id, start_time, end_time):
    reservations = get_reservation_by_time(start_time, end_time)
    for i in reservations:
        if i.classroomId == classrooom_id and i.status == ReservationStatus.Reserved or i.status == ReservationStatus.Pending:
            return True
    return False

def new_booking(user_id, classroom_id, time_period, date):
    if not date:
        raise BusinessError("date is required", 400)
    for i in time_period:
        start_time = add_time(date, time_slot_map[i]['start'])
        end_time = add_time(date, time_slot_map[i]['end'])
        reservation = get_certain_reservation(int(classroom_id), start_time, end_time)
        if reservation and (reservation.status == ReservationStatus.Reserved or reservation.status == ReservationStatus.Pending):
            raise BusinessError("a reservation is already existed", 400)
        try:
            classroom = get_classroom_by_id(classroom_id)
            if classroom.isRestricted:
                status = ReservationStatus.Pending
            else:
                status = ReservationStatus.Reserved
            reservation = add_reservation(int(user_id), int(classroom_id), start_time, end_time, status)
        except Exception as e:
            raise BusinessError("failed to make a reservation " + str(e),400)

    return reservation
