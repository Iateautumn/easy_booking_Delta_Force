# models/classroom.py
from app.extensions import db
from datetime import datetime



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



class Classroom(db.Model):

    __tablename__ = 'classroom'
    
    classroomId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classroomNumber = db.Column(db.String(20), nullable=False)
    building = db.Column(db.String(50), nullable=False)
    typeId = db.Column(db.Integer, db.ForeignKey('classroomType.typeId'), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean, default=False)

    classroomType = db.relationship('ClassroomType')

    def __init__(self, classroomNumber, building, typeId):
        self.classroomNumber = classroomNumber
        self.building = building
        self.typeId = typeId
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        self.isDeleted = False

def get_all_classeooms():
    list_classroom = Classroom.query.all()
    return list_classroom

def add_classroom(classroomNumber, building, typeId):
    new_classroom = Classroom(classroomNumber, building, typeId)
    db.session.add(new_classroom)
    db.session.commit()
    return new_classroom

def get_classroom_by_id(classroomId):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    return classroom

def get_classroom_by_number(classroomNumber):
    classroom = Classroom.query.filter_by(classroomNumber=classroomNumber).first()
    return classroom
def get_classroom_by_building(building):
    list_classroom = Classroom.query.filter_by(building=building).all()
    return list_classroom

def get_classroom_by_type_id(typeId):
    list_classroom = Classroom.query.filter_by(typeId=typeId).all()
    return list_classroom

def delete_classroom(classroomId):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    classroom.isDeleted = True
    db.session.commit()
    return classroom

def update_classroom(classroomId = None, classroomNumber = None, building = None, typeId = None):
    classroom = Classroom.query.filter_by(classroomId=classroomId).first()
    if classroom is None:
        return False
    if classroomNumber is not None:
        classroom.classroomNumber = classroomNumber
    if building is not None:
        classroom.building = building
    if typeId is not None:
        classroom.typeId = typeId
    classroom.updatedAt = datetime.now()
    db.session.commit()
    return classroom