from app.booking.models import get_reservation_by_user_id
from app.utils.exceptions import BusinessError
from app.classroom.models import get_classroom_by_id
from app.utils.datetime_utils import get_date_time, get_time_slot
def own_reservations(user_id):
    try:
        reservations = get_reservation_by_user_id(user_id)
        print(reservations)
    except Exception as e:
        raise BusinessError("error: " + str(e), 500)

    def reservation_to_dict(reservation):
        result = {
            "reservationId": reservation.reservationId,
            "status": str(reservation.status),
            "roomName": get_classroom_by_id(reservation.classroomId).classroomName,
            "date": get_date_time(str(reservation.startTime))[0],
            "timePeriod": get_time_slot(str(reservation.startTime)),
            "capacity": get_classroom_by_id(reservation.classroomId).capacity,
            "equipment": [equipment.equipmentName for equipment in get_classroom_by_id(reservation.classroomId).Equipments],
            "isRestricted": get_classroom_by_id(reservation.classroomId).isRestricted,
            "constrain": get_classroom_by_id(reservation.classroomId).constrain,
        }
        return result

    result = [reservation_to_dict(reservation) for reservation in reservations]
    return result
