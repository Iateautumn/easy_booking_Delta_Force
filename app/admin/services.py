from datetime import datetime
from typing import NewType

from app.auth.models import User, get_user_by_id, UserStatus
from app.booking.models import (
Reservation, 
ReservationStatus, 
get_reservation_by_status,
get_reservation_by_id,
update_reservation)
from app.classroom.models import delete_classroom,add_classroom, get_classroom_by_id, add_classequipment, update_classroom,delete_classequipment, get_classequipment_by_classroom_id, add_equipment
from app.utils.datetime_utils import slot_time_map, get_time_slot, get_date_time
from app.utils.exceptions import BusinessError


def get_reservation_requests():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Pending)
        print(reservations)
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
                "date": get_date_time(str(reservation.startTime))[0],
                "timePeriod": get_time_slot(str(reservation.startTime))
            }
            reservation_info_list.append(reservation_data)
        for reservation in reservations:
            get_dict(reservation)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return reservation_info_list


def approve_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Reserved)

        # reservation.status = ReservationStatus.Approved
        
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
    

def reject_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Rejected)
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
         


def add_room(classroom_name, capacity, equipment=[], new_equipment = [], constrain = ''):

    try:
        new_classroom = add_classroom(
            classroomName=classroom_name,
            capacity=capacity
        )
        # new_classroom.updatedAt = datetime.now()
        for new_equipment_name in new_equipment:
            new_equipment_instance = add_equipment(new_equipment_name)
            equipment.append(new_equipment_instance.equipmentId)
        for equip_id in equipment:
            add_classequipment(
                classroomId=new_classroom.classroomId,
                equipmentId=equip_id

            )
        return [str(classroom_name)]
    except Exception as e:
        raise BusinessError("Add room error: " + str(e), 500)


def modify_room(classroom_id, classroom_name=None, capacity=None,
                equipment=[], new_equipment = [], constrain=''):

    # if current_user.status != UserStatus.Admin.value:
    #     return {"status": "error", "message": "no admin power"}, 403

    try:
        update_classroom(
            classroomId=classroom_id,
            classroomName=classroom_name,
            capacity=capacity
        )

        my_equipments = get_classequipment_by_classroom_id(classroom_id)
        for my_equipment in my_equipments:
            delete_classequipment(my_equipment.classEquipmentId)

        for new_equipment_name in new_equipment:
            new_equipment_instance = add_equipment(new_equipment_name)
            equipment.append(new_equipment_instance.equipmentId)
        for equip_id in equipment:
            add_classequipment(
                classroomId=classroom_id,
                equipmentId=equip_id
            )

    except Exception as e:
        raise BusinessError("Add room error: " + str(e), 500)



def delete_room(classroom_id):
        try:

            classroom = get_classroom_by_id(classroom_id)

            delete_classroom(classroom_id)

            equipment_relations = get_classequipment_by_classroom_id(classroom_id)
            for relation in equipment_relations:
                delete_classequipment(relation.classEquipmentId)

        except Exception as e:
            raise BusinessError("Server error: " + str(e), 500)


# def get_all_rooms():
#
#     # if current_user.status != UserStatus.Admin.value:
#     #     return {"status": "error", "message": "no admin power"}, 403
#
#     try:
#
#         classroom_data = []
#         for room in all_classrooms:
#             valid_equipments = [
#                 {"id": eq.equipmentId, "name": eq.equipmentName}
#                 for eq in room.Equipments if not eq.isDeleted
#             ]
#
#             classroom_data.append({
#                 "id": room.classroomId,
#                 "name": room.classroomName,
#                 "capacity": room.capacity,
#                 "constrain": room.constrain,
#                 "is_restricted": room.isRestricted,
#                 "status": "active" if not room.isDeleted else "deleted",
#                 "equipments": valid_equipments,
#                 "created_at": room.createdAt.isoformat() if room.createdAt else None,
#                 "updated_at": room.updatedAt.isoformat() if room.updatedAt else None
#             })
#
#         return {
#             "data": classroom_data
#         }
#
#     except Exception as e:
#         return {"status": "error", "message": f" no found in database asset: {str(e)}"}, 500

