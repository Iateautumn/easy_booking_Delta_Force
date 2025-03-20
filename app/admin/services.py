from datetime import datetime
from typing import NewType

from app.auth.models import User, get_user_by_id, UserStatus
from app.auth.models import User, get_user_by_id
from app.booking.models import (
Reservation, 
ReservationStatus, 
get_reservation_by_status,
get_reservation_by_id,
update_reservation)
from app.classroom.models import delete_classroom, add_classroom, get_classroom_by_id, add_classequipment, \
    update_classroom, delete_classequipment, get_classequipment_by_classroom_id, add_equipment, get_all_classrooms, \
    get_classequipment_by_classroom_id_and_equipment_id
from app.utils.datetime_utils import slot_time_map, get_time_slot, get_date_time
from app.classroom.models import Classroom, get_classroom_by_id
from app.utils.datetime_utils import slot_time_map, get_time_slot
from app.utils.exceptions import BusinessError

import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def get_reservation_requests():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Pending)
        reservation_info_list = []
        def get_dict(reservation):
            userId = reservation.userId
            classroomId = reservation.classroomId
            user = get_user_by_id(userId)
            classroom = get_classroom_by_id(classroomId)
            reservation_data = {
                "reservationId": reservation.reservationId,
                "constrain": classroom.constrain,
                "classroomName": classroom.classroomName,
                "username": user.name,
                "userstatus": user.status.value,
                "date": get_date_time(str(reservation.startTime))[0],
                "timePeriod": get_time_slot(str(reservation.startTime))
            }
            reservation_info_list.append(reservation_data)
        for reservation in reservations:
            get_dict(reservation)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return reservation_info_list


def approve_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Reserved)

        # reservation.status = ReservationStatus.Approved
        
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
    

def reject_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Rejected)
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
         


def add_room(classroom_name, capacity, equipment=[], new_equipment = [], constrain = ''):

    try:
        constrain = None if not constrain else constrain
        new_classroom = add_classroom(
            classroomName=classroom_name,
            capacity=capacity,
            constrain = constrain
        )
        # new_classroom.updatedAt = datetime.now()

        for new_equipment_name in new_equipment:
            if new_equipment_name:
                new_equipment_instance = add_equipment(new_equipment_name)
                equipment.append(new_equipment_instance.equipmentId)
        for equip_id in equipment:
            add_classequipment(
                classroomId=new_classroom.classroomId,
                equipmentId=equip_id

            )
        return [str(classroom_name)]
    except Exception as e:
        raise BusinessError("Add room error: " + str(e), 500)


def modify_room(classroom_id, classroom_name=None, capacity=None,
                equipment=[], new_equipment = [], constrain=''):

    # if current_user.status != UserStatus.Admin.value:
    #     return {"status": "error", "message": "no admin power"}, 403

    try:
        update_classroom(
            classroomId=classroom_id,
            classroomName=classroom_name,
            capacity=capacity,
            constrain = constrain
        )

        my_equipments = get_classequipment_by_classroom_id(classroom_id)
        for my_equipment in my_equipments:
            delete_classequipment(my_equipment.classEquipmentId)
        for new_equipment_name in new_equipment:
            if new_equipment_name:
                new_equipment_instance = add_equipment(new_equipment_name)
                equipment.append(new_equipment_instance.equipmentId)
        for equip_id in equipment:
            add_classequipment(
                classroomId=classroom_id,
                equipmentId=equip_id
            )

    except Exception as e:
        raise BusinessError("Add room error: " + str(e), 500)



def delete_room(classroom_id):
        try:

            classroom = get_classroom_by_id(classroom_id)

            delete_classroom(classroom_id)

            equipment_relations = get_classequipment_by_classroom_id(classroom_id)
            for relation in equipment_relations:
                delete_classequipment(relation.classEquipmentId)

        except Exception as e:
            raise BusinessError("Server error: " + str(e), 500)



def get_equipment_dict(equipment):
    result = {
        "equipmentId": equipment.equipmentId,
        "equipmentName": equipment.equipmentName,
        "createdAt": equipment.createdAt,
        "updatedAt": equipment.updatedAt,
        "isDeleted": equipment.isDeleted
    }
    return result


def get_all_rooms():

    # if current_user.status != UserStatus.Admin.value:
    #     return {"status": "error", "message": "no admin power"}, 403

    try:
        all_classrooms = get_all_classrooms()
        all_classrooms = [room for room in all_classrooms if room.isDeleted == False]
        classroom_data = []
        for room in all_classrooms:
         classroom_data.append({
            "capacity": room.capacity,
            "isDeleted": room.isDeleted,
            "equipments": [get_equipment_dict(equipment) for equipment in room.Equipments if get_classequipment_by_classroom_id_and_equipment_id(room.classroomId, equipment.equipmentId).isDeleted == False],
            "createdAt": room.createdAt,
            "updatedAt": room.updatedAt,
            "classroomName": room.classroomName,
            "classroomId": room.classroomId,
            "constrain": room.constrain,
            "isRestricted": room.isRestricted,
            })
        return classroom_data

    except Exception as e:
        return {"status": "error", "message": f" no found in database asset: {str(e)}"}, 500

### Admin can cancel reservations via reservation_id
def admin_cancel_reservation(reservation_id):
    try:
        reservations = get_reservation_by_status(ReservationStatus.Reserved)
        for reservation in reservations:
            if reservation.reservationId == reservation_id:
                update_reservation(reservation.reservationId, reservation.userId, reservation.classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Cancelled)
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)

def admin_reservation_all():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Reserved)

        reservation_info_list = []
        def get_dict(reservation):
            userId = reservation.userId
            classroomId = reservation.classroomId
            user = get_user_by_id(userId)
            classroom = get_classroom_by_id(classroomId)
            reservation_data = {
                "reservationId": reservation.reservationId,
                "constrain": classroom.constrain,
                "roomName": classroom.classroomName,
                "userName": user.name,
                "isRestricted": classroom.isRestricted,
                "capacity": classroom.capacity,
                "status": reservation.status.value,
                "date": get_date_time(str(reservation.startTime))[0],
                "equipment": [equipment.equipmentName for equipment in classroom.Equipments],
                "timePeriod": get_time_slot(str(reservation.startTime))
            }
            reservation_info_list.append(reservation_data)
        for reservation in reservations:
            get_dict(reservation)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return reservation_info_list

def admin_report_analysis():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Reserved)
        classroom_data = get_all_classrooms()
        classroom_data = [room for room in classroom_data if not room.isDeleted]
        classroom_data = sorted(classroom_data, key=lambda x: x.classroomId)
        classroom_data = {room.classroomId: room for room in classroom_data}
        time_map = slot_time_map()
        report = {room_id: {time: 0 for time in time_map} for room_id in classroom_data}

        # Populate the report with reservation data
        for reservation in reservations:
            classroom_id = reservation.classroomId
            start_time = reservation.startTime
            end_time = reservation.endTime
            time_slot = get_time_slot(str(start_time))
            date = get_date_time(str(start_time))[0]
            if date < datetime.now().date():
                continue
            start_time = time_map[time_slot]
            end_time = time_map[get_time_slot(str(end_time))]
            for i in range(start_time, end_time):
                report[classroom_id][i] += 1

        # Helper function to generate heatmap image and save it as a file
        def generate_heatmap_image(data, filename):
            plt.figure(figsize=(10, 1))
            plt.imshow([data], cmap="hot", aspect="auto")
            plt.axis("off")
            plt.savefig(filename, format="png", bbox_inches="tight", pad_inches=0)
            plt.close()

        # Prepare separateData and save heatmap images
        separate_data = []
        for room_id, usage_data in report.items():
            room_name = classroom_data[room_id]["classroomName"]
            heat_graph = list(usage_data.values())
            usage = sum(heat_graph)
            heatmap_filename = f"{room_name}_heatmap.png"
            generate_heatmap_image(heat_graph, heatmap_filename)
            separate_data.append({
                "roomName": room_name,
                "usage": usage,
                "heatGraph": heatmap_filename
            })

        # Prepare jointData and save the joint heatmap image
        joint_heat_graph = [0] * len(time_map)
        for usage_data in report.values():
            for i, usage in enumerate(usage_data.values()):
                joint_heat_graph[i] += usage

        joint_heatmap_filename = "joint_heatmap.png"
        generate_heatmap_image(joint_heat_graph, joint_heatmap_filename)

        joint_data = {
            "heatGraph": joint_heatmap_filename
        }

        # Export data to a PDF
        pdf_filename = "admin_report_analysis.pdf"
        pdf_path = os.path.join(os.getcwd(), pdf_filename)
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(50, 750, "Admin Report Analysis")
        c.drawString(50, 730, "Separate Data:")

        y_position = 710
        for room in separate_data:
            c.drawString(50, y_position, f"Room Name: {room['roomName']}, Usage: {room['usage']}")
            y_position -= 20
            c.drawImage(room["heatGraph"], 50, y_position - 50, width=400, height=50)
            y_position -= 70
            if y_position < 100:  # Add a new page if space is insufficient
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = 750

        c.drawString(50, y_position, "Joint Data:")
        y_position -= 20
        c.drawImage(joint_data["heatGraph"], 50, y_position - 50, width=400, height=50)

        c.save()

        return {
            "separateData": separate_data,
            "jointData": joint_data,
            "pdfReportPath": pdf_path
        }

    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)
    
