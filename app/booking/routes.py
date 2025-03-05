# app/classrooms/routes.py
from flask import Blueprint, request, jsonify
from .services import (
    get_all_classrooms,
    filter_classrooms
)

classroom_bp = Blueprint('classrooms', __name__)


@classroom_bp.route('/classrooms', methods=['GET'])
def list_classrooms():

    capacity_min = request.args.get('capacity_min', type=int)
    capacity_max = request.args.get('capacity_max', type=int)
    equipment = request.args.getlist('equipment')
    days = request.args.getlist('days')

    classrooms = filter_classrooms(
        capacity_range=(capacity_min, capacity_max),
        equipment=equipment,
        days=days
    )

    return jsonify([c.to_dict() for c in classrooms])