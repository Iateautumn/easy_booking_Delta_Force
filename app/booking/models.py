# models/booking.py
from app import db,app
from datetime import datetime
from enum import Enum


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


def each_classroom_info(list_classroom):
    result = ''
    for classroom in list_classroom:
        result += f'Classroom Number: {classroom.classroomNumber}\n'
        result += f'Building: {classroom.building}\n'
        result += f'Type: {classroom.classroomType.typeName}\n'
        result += f'Capacity: {classroom.classroomType.capacity}\n'
        result += f'Equipment: {classroom.classroomType.equipment}\n'
        result += f'Created At: {classroom.createdAt}\n'
        result += f'Updated At: {classroom.updatedAt}\n'
        result += f'Is Deleted: {classroom.isDeleted}\n\n'
    return result


@app.route('/classroom_model')
def index2():
    return each_classroom_info(get_all_classeooms())


# if __name__ == '__main__':
    
#     app.run(debug=True)



