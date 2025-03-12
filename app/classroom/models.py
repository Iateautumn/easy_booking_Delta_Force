# models/classroom.py
from app.extensions import db
from datetime import datetime
# from app.auth.models import User
# from app.booking.models import Reservation

"""
class ClassroomType(db.Model):
    __tablename__ = 'classroomType'
    
    typeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typeName = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, typeName, capacity, equipment):
        self.typeName = typeName
        self.capacity = capacity
        self.equipment = equipment
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

def get_all_classroom_types():
    list_classroom_type = ClassroomType.query.all()
    return list_classroom_type

def add_classroom_type(typeName, capacity, equipment):
    new_classroom_type = ClassroomType(typeName, capacity, equipment)
    db.session.add(new_classroom_type)
    db.session.commit()
    return new_classroom_type

def get_classroom_type_by_id(typeId):
    classroom_type = ClassroomType.query.filter_by(typeId=typeId).first()
    return classroom_type

def get_classroom_type_by_name(typeName):
    classroom_type = ClassroomType.query.filter_by(typeName=typeName).first()
    return classroom_type

def delete_classroom_type(typeId):
    classroom_type = ClassroomType.query.filter_by(typeId=typeId).first()
    classroom_type.isDeleted = True
    db.session.commit()
    return classroom_type

def get_classroom_type_by_capacity(capacity):
    list_classroom_type = ClassroomType.query.filter(ClassroomType.capacity>=capacity).all()
    return list_classroom_type

def update_classroom_type(typeId, typeName, capacity, equipment):
    classroom_type = ClassroomType.query.filter_by(typeId=typeId).first()
    if classroom_type is None:
        return False
    if typeName is not None:
        classroom_type.typeName = typeName
    if capacity is not None:
        classroom_type.capacity = capacity
    if equipment is not None:
        classroom_type.equipment = equipment
    classroom_type.updatedAt = datetime.now()
    db.session.commit()
    return classroom_type
"""

class Equipment(db.Model):
    __tablename__ = 'equipment'
    equipmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipmentName = db.Column(db.String(50), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)
    Classrooms = db.relationship(
        "Classroom", 
        secondary="classequipment",
        back_populates="Equipments"  # 
    )

    def __init__(self, equipmentName):
        self.equipmentName = equipmentName
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

def get_all_equipments():
    list_equipment = Equipment.query.all()
    return list_equipment

def add_equipment(equipmentName):
    new_equipment = Equipment(equipmentName)
    db.session.add(new_equipment)
    db.session.commit()
    return new_equipment

def get_equipment_by_id(equipmentId):
    equipment = Equipment.query.filter_by(equipmentId=equipmentId).first()
    return equipment

def get_equipment_by_name(equipmentName):
    equipment = Equipment.query.filter_by(equipmentName=equipmentName).first()
    return equipment

def delete_equipment(equipmentId):
    equipment = Equipment.query.filter_by(equipmentId=equipmentId).first()
    equipment.isDeleted = True
    db.session.commit()
    return equipment

def update_equipment(equipmentId, equipmentName):
    equipment = Equipment.query.filter_by(equipmentId=equipmentId).first()
    if equipment is None:
        return False
    if equipmentName is not None:
        equipment.equipmentName = equipmentName
    equipment.updatedAt = datetime.now()
    db.session.commit()
    return equipment



class Classroom(db.Model):

    __tablename__ = 'classroom'
    
    classroomId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroomName = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    constrain= db.Column(db.String(50))
    isRestricted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)
    # Users = db.relationship(
    #     "User",
    #     secondary="reservation",
    #     back_populates="Classrooms"  # back_populates
    # )
    Equipments = db.relationship(
        "Equipment",
        secondary="classequipment",
        back_populates="Classrooms"  # back_populates
    )

    def __init__(self, classroomName, capacity):
        self.classroomName = classroomName
        self.capacity = capacity
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False
    
    @property
    def users(self):
        from app.auth.models import User
        from app.booking.models import Reservation
        return User.query.join(Reservation).filter(Reservation.classroomId == self.classroomId).all()


def get_all_classrooms():
    list_classroom = Classroom.query.all()
    return list_classroom

def add_classroom(classroomName, capactiy):
    new_classroom = Classroom(classroomName, capactiy)
    db.session.add(new_classroom)
    db.session.commit()
    return new_classroom

def get_classroom_by_id(classroomId):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    return classroom

def get_classroom_by_name(classroomName):
    classroom = Classroom.query.filter_by(classroomName=classroomName).first()
    return classroom

def get_classroom_by_capacity(capacity):
    list_classroom = Classroom.query.filter_by(capacity>capacity).all()
    return list_classroom


# def get_classroom_by_building(building):
#     list_classroom = Classroom.query.filter_by(building=building).all()
#     return list_classroom

# def get_classroom_by_type_id(typeId):
#     list_classroom = Classroom.query.filter_by(typeId=typeId).all()
#     return list_classroom

def delete_classroom(classroomId):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    classroom.isDeleted = True
    db.session.commit()
    return classroom

def update_classroom(classroomId = None, classroomName = None, capacity = None):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    if classroom is None:
        return False
    if classroomName is not None:
        classroom.classroomNumber = classroomName
    if capacity is not None:
        classroom.capacity = capacity

    classroom.updatedAt = datetime.now()
    db.session.commit()
    return classroom

def get_classroom_by_filter(classroomName=None, capacity=None, isRestricted=None):
    query = Classroom.query  
    
    if classroomName is not None:
        query = query.filter_by(classroomName=classroomName)  
    if capacity is not None:
        query = query.filter_by(capacity=capacity)  
    if isRestricted is not None:
        query = query.filter_by(isRestricted=isRestricted)  
    list_classroom = query.all()  
    return list_classroom


class ClassEquipment(db.Model):
    __tablename__ = 'classequipment'
    classEquipmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroomId = db.Column(db.Integer, db.ForeignKey('classroom.classroomId'), nullable=False)
    equipmentId = db.Column(db.Integer, db.ForeignKey('equipment.equipmentId'), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, classroomId, equipmentId):
        self.classroomId = classroomId
        self.equipmentId = equipmentId
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

def add_classequipment(classroomId, equipmentId):
    new_classequipment = ClassEquipment(classroomId, equipmentId)
    db.session.add(new_classequipment)
    db.session.commit()
    return new_classequipment

def get_classequipment_by_id(classEquipmentId):
    classequipment = ClassEquipment.query.filter_by(classEquipmentId=classEquipmentId).first()
    return classequipment

def delete_classequipment(classEquipmentId):
    classequipment = ClassEquipment.query.filter_by(classEquipmentId=classEquipmentId).first()
    classequipment.isDeleted = True
    db.session.commit()
    return classequipment

def update_classequipment(classEquipmentId, classroomId = None, equipmentId = None):
    classequipment = ClassEquipment.query.filter_by(classEquipmentId=classEquipmentId).first()
    if classequipment is None:
        return False
    if classroomId is not None:
        classequipment.classroomId = classroomId
    if equipmentId is not None:
        classequipment.equipmentId = equipmentId
    classequipment.updatedAt = datetime.now()
    db.session.commit()
    return classequipment

def get_classequipment_by_classroom_id(classroomId):
    list_classequipment = ClassEquipment.query.filter_by(classroomId=classroomId).all()
    return list_classequipment

def get_classequipment_by_equipment_id(equipmentId):
    list_classequipment = ClassEquipment.query.filter_by(equipmentId=equipmentId).all()
    return list_classequipment






