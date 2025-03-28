from app.booking.models import get_reservation_by_user_id, update_reservation,get_reservation_by_id, cancel_reservation,get_reservation_by_filter
from app.utils.exceptions import BusinessError
from app.classroom.models import get_classroom_by_id
from app.utils.datetime_utils import get_date_time, get_time_slot, add_time, time_slot_map
from ics import Calendar, Event
import tempfile
from datetime import datetime, timedelta
from app.booking.models import ReservationStatus
from app.auth.models import get_issue_report_by_filter, get_issue_report_by_id, update_issue_report, add_issue_report
from app.auth.models import get_user_by_id, UserStatus
def to_calendar(user_id, reservation_ids=[]):
    try:
        if reservation_ids:
            reservations = [get_reservation_by_id(reservation_id) for reservation_id in reservation_ids]
        else: 
            reservations = get_reservation_by_filter(userId=user_id, status=ReservationStatus.Reserved)
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)

    def reservation_to_dict(reservation):
        classroom = get_classroom_by_id(reservation.classroomId)
        result = {
            "classroomName": classroom.classroomName,
            "date": get_date_time(str(reservation.startTime))[0],

            "startTime": get_date_time(str(reservation.startTime))[1],
            "endTime": get_date_time(str(reservation.endTime))[1],
            "equipment": [equipment.equipmentName for equipment in classroom.Equipments],
            "constrain": classroom.constrain,
        }
        return result
    meta_data = [reservation_to_dict(reservation) for reservation in reservations]
    calendar = Calendar()

    for reservation in meta_data:
        event = Event()
        event.name = f"Reservation: {reservation['classroomName']}"
        event.begin = datetime.strptime(f"{reservation['date']} {reservation['startTime']}",
                                        "%Y-%m-%d %H:%M:%S") - timedelta(hours=8)
        event.end = datetime.strptime(f"{reservation['date']} {reservation['endTime']}",
                                      "%Y-%m-%d %H:%M:%S") - timedelta(hours=8)
        event.description = (
            f"Classroom: {reservation['classroomName']}\n"
            f"Equipment: {', '.join(reservation['equipment'])}\n"
            f"Constraints: {reservation['constrain']}"
        )
        calendar.events.add(event)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ics", mode='w') as temp_file:
        temp_file.write(str(calendar))
        temp_file_path = temp_file.name
    
    return temp_file_path

def own_reservations(user_id):
    try:
        reservations = get_reservation_by_filter(userId=user_id, startTime=datetime.now())
        print(reservations)
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)

    def reservation_to_dict(reservation):
        classroom = reservation.classroom
        result = {
            "reservationId": reservation.reservationId,
            "status": str(reservation.status.value),
            "roomName": classroom.classroomName,
            "date": get_date_time(str(reservation.startTime))[0],
            "timePeriod": get_time_slot(str(reservation.startTime)),
            "capacity": classroom.capacity,
            "equipment": [equipment.equipmentName for equipment in classroom.Equipments],
            "isRestricted": classroom.isRestricted,
            "constrain": classroom.constrain,
            "issue": classroom.issue
        }
        return result
    result = [reservation_to_dict(reservation) for reservation in reservations]
    return result

def get_available_time_periods(reservation_id):
    try:
        reservation = get_reservation_by_id(reservation_id)
    except BusinessError as e:
        raise e
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)
    
    try:
        start = datetime.strptime(f"{reservation.startTime.strftime('%Y-%m-%d')} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(f"{reservation.endTime.strftime('%Y-%m-%d')} 23:59:59", "%Y-%m-%d %H:%M:%S")
        reservations = get_reservation_by_filter(
            classroomId=reservation.classroomId,
            startTime=start,
            endTime=end
        )
        reservations = [res for res in reservations if res.status != ReservationStatus.Cancelled]
    except BusinessError as e:
        raise e
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)
    
    now = datetime.now()
    time_periods = []
    for i in range(0, 10):
        if now > datetime.strptime(f"{reservation.startTime.strftime('%Y-%m-%d')} {time_slot_map[i]['start']}", "%Y-%m-%d %H:%M:%S"):
            continue
        time_periods.append(i)
    for res in reservations:
        time_slot = get_time_slot(str(res.startTime))
        print(time_slot)
        if time_slot in time_periods:
            time_periods.remove(time_slot)

    return time_periods

def modify_reservation(reservationId, userId, date, timePeriod):
    startTime = add_time(date, time_slot_map[int(timePeriod)]['start'])
    endTime = add_time(date, time_slot_map[int(timePeriod)]['end'])
    

    if endTime < datetime.now():
        raise BusinessError("cannot reserve past time", 400)
    
    try:
        reservation = get_reservation_by_id(reservationId)
        if userId != reservation.userId:
            raise BusinessError("You do not have this reservation: " + str(reservationId), 404)
    except BusinessError as e:
        raise e
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)
    try:

        user = get_user_by_id(userId)
        if  user.status != UserStatus.Admin:
            update_reservation(reservationId, userId, reservation.classroomId, add_time(date, time_slot_map[int(timePeriod)]['start']), add_time(date, time_slot_map[int(timePeriod)]['end']), ReservationStatus.Pending)
        else:
            update_reservation(reservationId, userId, reservation.classroomId,
                               add_time(date, time_slot_map[int(timePeriod)]['start']),
                               add_time(date, time_slot_map[int(timePeriod)]['end']), ReservationStatus.Reserved)
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)


def cancel_my_reservation(userId, reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        if userId != reservation.userId:
            raise BusinessError("You do not have this reservation: " + str(reservationId), 404)
    except BusinessError as e:
        raise e
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)

    try:
        cancel_reservation(reservationId)
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)
    
def report_issue(userId, issue):
    try:
        add_issue_report(userId, issue)
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)


