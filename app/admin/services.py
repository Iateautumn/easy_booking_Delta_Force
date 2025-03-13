from app.auth.models import User, get_user_by_id
from app.booking.models import (
Reservation, 
ReservationStatus, 
get_reservation_by_status, 
get_reservation_by_id,
update_reservation)
from app.classroom.models import Classroom, get_classroom_by_id
from app.utils.datetime_utils import slot_time_map, get_time_slot
from app.utils.exceptions import BusinessError

### 这里的user是一个管理员admin，the administrator can approve the booking request for restricted rooms 

### 获取所有未处理的预约请求
def get_reservation_requests():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Pending)
        reservation_info_list = []
        def get_dict(reservation):
            userId = reservation.userId
            classroomId = reservation.classroomId
            user = get_user_by_id(userId)
            classroom = get_classroom_by_id(classroomId)
            reservation_data = {
                "reservationId": reservation.reservationId,
                "constrain": classroom.constrain,
                "classroomName": classroom.classroomName,
                "username": user.name,
                "userstatus": user.status.value,
                "date": str(reservation.startTime),
                "timePeriod": get_time_slot(str(reservation.startTime))
            }
            reservation_info_list.append(reservation_data)
        for reservation in reservations:
            get_dict(reservation)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return reservation_info_list

### 同意预约请求
def approve_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Reserved)

        # reservation.status = ReservationStatus.Approved
        
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
    

### 拒绝预约请求
def reject_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Rejected)
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
         
