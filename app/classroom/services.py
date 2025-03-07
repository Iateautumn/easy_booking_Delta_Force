# app/classrooms/services.py
from app.classroom.models import Classroom, get_all_equipments, ClassEquipment
from sqlalchemy import and_

def filter_classrooms(capacity_range = [0, 9999], equipments = [], days = []):
    query = Classroom.query

    if capacity_range[0]:
        query = query.filter(Classroom.capacity >= capacity_range[0])
    if capacity_range[1]:
        query = query.filter(Classroom.capacity <= capacity_range[1])

    if equipments:

        conditions = [ClassEquipment.equipmentId == eq_id for eq_id in equipments]
        query = query.join(ClassEquipment).filter(and_(*conditions))

    if days:
        query = query.filter(Classroom.opening_days.overlap(days))

    classrooms = query.all()
    classrooms_dict = [classroom.to_dict() for classroom in classrooms]

    return classrooms_dict

def get_all_equipments():
    return get_all_equipments()