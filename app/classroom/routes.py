# app/classrooms/routes.py
from flask import Blueprint, request, jsonify
from app.utils.response import success_response, error_response
from app.classroom.services import (
    get_equipments,
    filter_classrooms
)

classroom_bp = Blueprint('classroom', __name__, url_prefix='/classroom')

@classroom_bp.route('/filter', methods=['GET','POST'])
def list_classrooms():
    if request.method == 'GET':
        classrooms = filter_classrooms()
        #import pdb; pdb.set_trace()
        return success_response(classrooms)
    elif request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            return error_response('Unresolvable request body',400)

        capacity_min = data['capacity_min']
        capacity_max = data['capacity_max']
        equipments = data['equipment']
        date = data['date']


        classrooms = filter_classrooms(
            capacity_range=[capacity_min, capacity_max],
            equipments=equipments,
            date=date
        )

    return success_response(classrooms)

@classroom_bp.route('/equipment', methods=['GET'])
def get_all_equipments():
    if request.method == 'GET':
        return success_response(get_equipments())

