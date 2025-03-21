from datetime import datetime
from typing import NewType

from app.auth.models import User, get_user_by_id, UserStatus
from app.auth.models import User, get_user_by_id
from app.booking.models import (
Reservation, 
ReservationStatus, 
get_reservation_by_status,
get_reservation_by_id,
update_reservation)
from app.classroom.models import delete_classroom, add_classroom, get_classroom_by_id, add_classequipment, \
    update_classroom, delete_classequipment, get_classequipment_by_classroom_id, add_equipment, get_all_classrooms, \
    get_classequipment_by_classroom_id_and_equipment_id
from app.utils.datetime_utils import slot_time_map, get_time_slot, get_date_time
from app.classroom.models import Classroom, get_classroom_by_id, add_issue
from app.utils.datetime_utils import slot_time_map, get_time_slot
from app.utils.exceptions import BusinessError
from app.auth.models import get_issue_report_by_filter, get_issue_report_by_id, delete_issue_report, add_issue_report


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
        constrain = None if not constrain else constrain
        new_classroom = add_classroom(
            classroomName=classroom_name,
            capacity=capacity,
            constrain = constrain
        )
        # new_classroom.updatedAt = datetime.now()

        for new_equipment_name in new_equipment:
            if new_equipment_name:
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
                equipment=[], new_equipment = [], constrain='', issue=''):

    # if current_user.status != UserStatus.Admin.value:
    #     return {"status": "error", "message": "no admin power"}, 403

    try:
        update_classroom(
            classroomId=classroom_id,
            classroomName=classroom_name,
            capacity=capacity,
            constrain = constrain,
        )

        add_issue(classroom_id, issue)

        my_equipments = get_classequipment_by_classroom_id(classroom_id)
        for my_equipment in my_equipments:
            delete_classequipment(my_equipment.classEquipmentId)
        for new_equipment_name in new_equipment:
            if new_equipment_name:
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



def get_equipment_dict(equipment):
    result = {
        "equipmentId": equipment.equipmentId,
        "equipmentName": equipment.equipmentName,
        "createdAt": equipment.createdAt,
        "updatedAt": equipment.updatedAt,
        "isDeleted": equipment.isDeleted
    }
    return result


def get_all_rooms():

    # if current_user.status != UserStatus.Admin.value:
    #     return {"status": "error", "message": "no admin power"}, 403

    try:
        all_classrooms = get_all_classrooms()
        all_classrooms = [room for room in all_classrooms if room.isDeleted == False]
        classroom_data = []
        for room in all_classrooms:
         classroom_data.append({
            "capacity": room.capacity,
            "isDeleted": room.isDeleted,
            "equipments": [get_equipment_dict(equipment) for equipment in room.Equipments if get_classequipment_by_classroom_id_and_equipment_id(room.classroomId, equipment.equipmentId).isDeleted == False],
            "createdAt": room.createdAt,
            "updatedAt": room.updatedAt,
            "classroomName": room.classroomName,
            "classroomId": room.classroomId,
            "constrain": room.constrain,
            "isRestricted": room.isRestricted,
            "issue": room.issue
            })
        return classroom_data

    except Exception as e:
        return {"status": "error", "message": f" no found in database asset: {str(e)}"}, 500

### Admin can cancel reservations via reservation_id
def admin_cancel_reservation(reservation_id):
    try:
        reservations = get_reservation_by_status(ReservationStatus.Reserved)
        for reservation in reservations:
            if reservation.reservationId == reservation_id:
                update_reservation(reservation.reservationId, reservation.userId, reservation.classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Cancelled)
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)

def admin_reservation_all():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Reserved)

        reservation_info_list = []
        def get_dict(reservation):
            userId = reservation.userId
            classroomId = reservation.classroomId
            user = get_user_by_id(userId)
            classroom = get_classroom_by_id(classroomId)
            reservation_data = {
                "reservationId": reservation.reservationId,
                "constrain": classroom.constrain,
                "roomName": classroom.classroomName,
                "userName": user.name,
                "isRestricted": classroom.isRestricted,
                "capacity": classroom.capacity,
                "status": reservation.status.value,
                "date": get_date_time(str(reservation.startTime))[0],
                "equipment": [equipment.equipmentName for equipment in classroom.Equipments],
                "timePeriod": get_time_slot(str(reservation.startTime)),
                "issue": classroom.issue
            }
            reservation_info_list.append(reservation_data)
        for reservation in reservations:
            get_dict(reservation)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return reservation_info_list

# def admin_reservation_requests():
#     try:
#         reservations = get_reservation_by_status(ReservationStatus.Pending)
#         reservation_info_list = []
#         def get_dict(reservation):
#             userId = reservation.userId
#             classroomId = reservation.classroomId
#             user = get_user_by_id(userId)
#             classroom = get_classroom_by_id(classroomId)
#             reservation_data = {
#                 "reservationId": reservation.reservationId,
#                 "constrain": classroom.constrain,
#                 "classroomName": classroom.classroomName,
#                 "userName": user.name,
#                 "userstatus": user.status,
#                 "date": get_date_time(str(reservation.startTime))[0],
#                 "timePeriod": get_time_slot(str(reservation.startTime)),
#                 "issue": classroom.issue
#             }
#             reservation_info_list.append(reservation_data)
#         for reservation in reservations:
#             get_dict(reservation)
#     except Exception as e:
#         raise BusinessError("Service error: " + str(e), 500)

#     return reservation_info_list

def get_reported_issue():
    try:
        issue_reports = get_issue_report_by_filter()
        issue_report_list = []
        def get_dict(issue_report):
            userId = issue_report.userId
            user = get_user_by_id(userId)
            issue_report_data = {
                "issueId": issue_report.reportId,
                "userName": user.name,
                "issue": issue_report.description,
                "date": get_date_time(str(issue_report.createdAt), origin_format="%Y-%m-%d")[0]
            }
            issue_report_list.append(issue_report_data)
        for issue_report in issue_reports:
            if issue_report.isDeleted == False:
                get_dict(issue_report)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return issue_report_list

def delete_reported_issue(issue_id):
    try:
        delete_issue_report(issue_id)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)