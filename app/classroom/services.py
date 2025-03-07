# app/classrooms/services.py
from app.classroom.models import Classroom, get_all_equipments



def filter_classrooms(capacity_range, equipment, days):
    query = Classroom.query

    # 容量过滤
    if capacity_range[0]:
        query = query.filter(Classroom.capacity >= capacity_range[0])
    if capacity_range[1]:
        query = query.filter(Classroom.capacity <= capacity_range[1])

    if equipment:
        query = query.filter(Classroom.equipment.contains(equipment))

    if days:
        query = query.filter(Classroom.opening_days.overlap(days))

    return query.all()

def get_all_equipments():
    return get_all_equipments()