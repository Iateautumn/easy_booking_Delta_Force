# app/bookings/services.py
from datetime import datetime
from app.utils.exceptions import BusinessError
from sqlalchemy import and_
from werkzeug.http import parse_age
from app.booking.models import add_reservation, get_reservation_by_time, ReservationStatus
from app.utils.datetime_utils import time_slot_map, add_time, slot_time_map, get_current_date
from app.extensions import db
from app.classroom.models import get_classroom_by_id
from app.auth.models import get_user_by_id
from app.auth.services import send_email_sync
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def get_certain_reservation(classrooom_id, start_time, end_time):
    reservations = get_reservation_by_time(start_time, end_time)
    for i in reservations:
        if i.classroomId == classrooom_id and i.status == ReservationStatus.Reserved or i.status == ReservationStatus.Pending:
            return True
    return False

async def new_booking(user_id, classroom_id, time_period, date):
    if not date:
        raise BusinessError("date is required", 400)
    for i in time_period:
        start_time = add_time(date, time_slot_map[i]['start'])
        end_time = add_time(date, time_slot_map[i]['end'])
        reservation = get_certain_reservation(int(classroom_id), start_time, end_time)
        
        if end_time < datetime.now():
            raise BusinessError("cannot reserve past time", 400)
        
        if reservation:
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
    if reservation.status == ReservationStatus.Reserved:
        await reservation_email_async(reservation, 'Your classroom reservation has been confirmed.')
    return reservation

async def reservation_email_async(reservation, msg):
    
    user = get_user_by_id(reservation.userId)

    from_name = user.name
    from_addr = "1534433057@qq.com"
    from_pwd = "oeisscrfcfukgccf"
    to_addr = user.email
    my_title = "Reservation Success"
    my_msg = f"""
Hello, {user.name}! f{msg}
Reservation Details:
Classroom ID: {reservation.classroomId}
Start Time: {reservation.startTime}
End Time: {reservation.endTime}
Thank you for using our service.
"""

    msg = MIMEText(my_msg, 'plain', 'utf-8')
    msg['From'] = formataddr([from_name, from_addr])
    msg['To'] = to_addr
    msg['Subject'] = my_title

    smtp_srv = "smtp.qq.com"

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, send_email_sync, smtp_srv, from_addr, from_pwd, to_addr, msg)
    except Exception as e:
        raise BusinessError(f"Failed to send email: {str(e)}", 500)