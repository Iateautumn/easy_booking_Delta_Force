from datetime import datetime


from app.auth.models import User, get_user_by_id, UserStatus
from app.booking.models import (
Reservation, 
ReservationStatus, 
get_reservation_by_status,
get_reservation_by_id,
update_reservation)
from app.classroom.models import Classroom, get_classroom_by_id, ClassEquipment
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
         


def add_room(current_user, classroom_name, capacity, equipment_ids=[], constrain=None, is_restricted=False):

    if current_user.status != UserStatus.Admin.value:
        return {"status": "error", "message": "no admin power"}, 403

    try:
        new_classroom = Classroom.add_classroom(
            classroomName=classroom_name,
            capacity=capacity
        )

        if constrain:
            new_classroom.constrain = constrain
        new_classroom.isRestricted = is_restricted
        new_classroom.updatedAt = datetime.now()

        for equip_id in equipment_ids:
            ClassEquipment.add_classequipment(
                classroomId=new_classroom.classroomId,
                equipmentId=equip_id
            )

        return {
            "code": 200,
            "message": "Classroom updated successfully",
            "data": [str(classroom_name)]
        }

    except Exception as e:
        raise BusinessError("Add room error: " + str(e), 500)


def modify_room(current_user, classroom_id, classroom_name=None, capacity=None,
                equipment_ids=None, constrain=None, is_restricted=None):

    if current_user.status != UserStatus.Admin.value:
        return {"status": "error", "message": "no admin power"}, 403

    try:
        updated = Classroom.update_classroom(
            classroomId=classroom_id,
            classroomName=classroom_name,
            capacity=capacity
        )

        classroom = Classroom.get_classroom_by_id(classroom_id)

        if constrain is not None:
            classroom.constrain = constrain
        if is_restricted is not None:
            classroom.isRestricted = is_restricted
        classroom.updatedAt = datetime.now()

        if equipment_ids is not None:
            existing_equipments = ClassEquipment.get_classequipment_by_classroom_id(classroom_id)
            for eq in existing_equipments:
                ClassEquipment.delete_classequipment(eq.classEquipmentId)

            for equip_id in equipment_ids:
                ClassEquipment.add_classequipment(
                    classroomId=classroom_id,
                    equipmentId=equip_id
                )


    except Exception as e:
        raise BusinessError("Add room error: " + str(e), 500)



def delete_room(current_user, classroom_id):
    def delete_room(current_user, request_data):
        if current_user.status != UserStatus.Admin.value:
            return {
                "code": 403,
                "message": "Permission denied",
                "data": []
            }

        try:

            classroom_id = request_data["classroom_id"]
            classroom = Classroom.get_classroom_by_id(classroom_id)


            Classroom.delete_classroom(classroom_id)


            equipment_relations = ClassEquipment.get_classequipment_by_classroom_id(classroom_id)
            for relation in equipment_relations:
                ClassEquipment.delete_classequipment(relation.classEquipmentId)

            return [str(classroom.classroomName)]

        except Exception as e:
            raise BusinessError("Server error: " + str(e), 500)


# def get_all_rooms(current_user):
#
#     if current_user.status != UserStatus.Admin.value:
#         return {"status": "error", "message": "no admin power"}, 403
#
#     try:
#         all_classrooms = Classroom.query.options(
#             db.joinedload(Classroom.Equipments)
#         ).order_by(Classroom.classroomId).all()
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
#             "status": "success",
#             "data": {
#                 "total": len(classroom_data),
#                 "classrooms": classroom_data
#             }
#         }, 200
#
#     except Exception as e:
#         return {"status": "error", "message": f" no found in database asset: {str(e)}"}, 500

