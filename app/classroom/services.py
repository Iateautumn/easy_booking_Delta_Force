# app/classrooms/services.py
from app.classroom.models import Classroom


def get_all_classrooms():
    classroom = Classroom()
    return classroom.get_all_classrooms()

def filter_classrooms(capacity_range, equipment, days):
    query = Classroom.query

    # 容量过滤
    if capacity_range[0]:
        query = query.filter(Classroom.capacity >= capacity_range[0])
    if capacity_range[1]:
        query = query.filter(Classroom.capacity <= capacity_range[1])

    # 设备过滤
    if equipment:
        query = query.filter(Classroom.equipment.contains(equipment))

    # 开放时间过滤（假设模型中有 opening_days 字段）
    if days:
        query = query.filter(Classroom.opening_days.overlap(days))

    return query.all()