
from pycparser.ply.yacc import resultlimit

from app.classroom.models import Classroom, get_all_equipments, ClassEquipment, get_timetable_by_classroom_name
from sqlalchemy import and_
from app.booking.models import get_reservation_by_classroom_id, ReservationStatus
from app.utils.datetime_utils import time_slot_map, slot_time_map, is_same_date, get_time_slot, get_current_date
from datetime import datetime

def filter_classrooms(capacity_range = [0, 9999], equipments = [], date = get_current_date(), issue=None):

    query = Classroom.query
    query = query.filter(Classroom.isDeleted == False)
    if capacity_range[0]:
        query = query.filter(Classroom.capacity >= capacity_range[0])
    if capacity_range[1]:
        query = query.filter(Classroom.capacity <= capacity_range[1])

    if equipments:

        conditions = [ClassEquipment.equipmentId == int(equipments[0])]
        query = query.join(ClassEquipment).filter(and_(*conditions))
    if not date:
        date = get_current_date()
    if issue is not None:
        if not issue:
            query = query.filter(Classroom.issue.is_(None) | (Classroom.issue == ""), Classroom.isDeleted == False)
        else:
            query = query.filter(Classroom.issue.isnot(None) & (Classroom.issue != ""), Classroom.isDeleted == False)
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
            "timePeriod": time_period,
            "issue": classroom.issue
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
        timetable_datas = get_timetable_by_classroom_name(classroom.classroomName)
        for timetable in timetable_datas:
            if not is_same_date(date, str(timetable.timeStamp)):
                continue
            b.append(get_time_slot(str(timetable.timeStamp)))
            b.append(get_time_slot(str(timetable.timeStamp)) + 1)
        if len(b) == len(slot_time_map.keys()):
            continue
        
        valid_time_slots = []
        for i in range(len(time_slot_map.keys())):
            starttime = time_slot_map[i]['start']
            starttime = datetime.strptime(starttime, '%H:%M:%S')
            
            require_date = datetime.strptime(date, '%Y-%m-%d')
            if starttime.time() < datetime.now().time() and require_date.date() <= datetime.now().date():
                continue
            if i not in b:
                valid_time_slots.append(i)

        result_classrooms.append(get_classroom_dict(classroom, valid_time_slots))

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