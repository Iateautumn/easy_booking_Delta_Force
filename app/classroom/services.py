
from pycparser.ply.yacc import resultlimit

from app.classroom.models import Classroom, get_all_equipments, ClassEquipment
from sqlalchemy import and_
from app.booking.models import get_reservation_by_classroom_id, ReservationStatus
from app.utils.datetime_utils import time_slot_map, slot_time_map, is_same_date, get_time_slot, get_current_date

def filter_classrooms(capacity_range = [0, 9999], equipments = [], date = get_current_date()):

    query = Classroom.query

    if capacity_range[0]:
        query = query.filter(Classroom.capacity >= capacity_range[0])
    if capacity_range[1]:
        query = query.filter(Classroom.capacity <= capacity_range[1])

    if equipments:

        conditions = [ClassEquipment.equipmentId == int(equipments[0])]
        query = query.join(ClassEquipment).filter(and_(*conditions))
    if not date:
        date = get_current_date()
    classrooms = query.all()
    result_classrooms = []
    for classroom in classrooms:
        classroom_equipments = [equipment.equipmentId for equipment in classroom.Equipments]
        state = True
        for equipment in equipments:
            if int(equipment) not in classroom_equipments:
                state = False
                break
        if state:
            result_classrooms.append(classroom)
    classrooms = result_classrooms


    def get_equipment_dict(equipment):
        result = {
            "equipmentId": equipment.equipmentId,
            "equipmentName": equipment.equipmentName,
            "createdAt": equipment.createdAt,
            "updatedAt": equipment.updatedAt,
            "isDeleted": equipment.isDeleted
        }
        return result

    def get_classroom_dict(classroom, time_period):
        result = {
            "classroomId": classroom.classroomId,
            "classroomName": classroom.classroomName,
            "createdAt": classroom.createdAt,
            "updatedAt": classroom.updatedAt,
            "isDeleted": classroom.isDeleted,
            "capacity": classroom.capacity,
            "constrain": classroom.constrain,
            "isRestricted": classroom.isRestricted,
            "equipments": [get_equipment_dict(equipment) for equipment in classroom.Equipments],
            "timePeriod": time_period
        }
        return result

    result_classrooms = []
    for classroom in classrooms:
        reservations = get_reservation_by_classroom_id(classroom.classroomId)
        b = []
        for reservation in reservations:
            if not is_same_date(date, str(reservation.startTime)):
                continue
            if reservation.status.value == ReservationStatus.Reserved.value or reservation.status.value == ReservationStatus.Pending.value:
                print(reservation.status)
                b.append(get_time_slot(str(reservation.startTime)))
        if len(b) == len(slot_time_map.keys()):
            continue

        result_classrooms.append(get_classroom_dict(classroom, [i for i in range(len(time_slot_map.keys())) if i not in b]))

    return result_classrooms

def get_equipments():
    equipments = get_all_equipments()
    equipments = [
        {
            "equipmentId": equipment.equipmentId,
            "equipmentName": equipment.equipmentName
        } for equipment in equipments
    ]

    return equipments