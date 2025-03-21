from datetime import datetime, timedelta
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
from app.classroom.models import Classroom, get_classroom_by_id, add_issue
from app.utils.datetime_utils import slot_time_map, get_time_slot
from app.utils.exceptions import BusinessError
from app.auth.models import get_issue_report_by_filter, get_issue_report_by_id, delete_issue_report, add_issue_report

import base64
from io import BytesIO
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from app.booking.services import reservation_email_async

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


async def approve_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Reserved)

        # reservation.status = ReservationStatus.Approved
        await reservation_email_async(reservation, 'Your classroom reservation has been approved by the administrator.')
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
    

async def reject_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Rejected)

        await reservation_email_async(reservation, 'Your classroom reservation has been rejected by the administrator.')
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
                equipment=[], new_equipment = [], constrain='', issue=''):

    # if current_user.status != UserStatus.Admin.value:
    #     return {"status": "error", "message": "no admin power"}, 403

    try:
        update_classroom(
            classroomId=classroom_id,
            classroomName=classroom_name,
            capacity=capacity,
            constrain = constrain,
        )

        add_issue(classroom_id, issue)

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
            "issue": room.issue
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
                "timePeriod": get_time_slot(str(reservation.startTime)),
                "issue": classroom.issue
            }
            reservation_info_list.append(reservation_data)
        for reservation in reservations:
            get_dict(reservation)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return reservation_info_list

# def admin_reservation_requests():
#     try:
#         reservations = get_reservation_by_status(ReservationStatus.Pending)
#         reservation_info_list = []
#         def get_dict(reservation):
#             userId = reservation.userId
#             classroomId = reservation.classroomId
#             user = get_user_by_id(userId)
#             classroom = get_classroom_by_id(classroomId)
#             reservation_data = {
#                 "reservationId": reservation.reservationId,
#                 "constrain": classroom.constrain,
#                 "classroomName": classroom.classroomName,
#                 "userName": user.name,
#                 "userstatus": user.status,
#                 "date": get_date_time(str(reservation.startTime))[0],
#                 "timePeriod": get_time_slot(str(reservation.startTime)),
#                 "issue": classroom.issue
#             }
#             reservation_info_list.append(reservation_data)
#         for reservation in reservations:
#             get_dict(reservation)
#     except Exception as e:
#         raise BusinessError("Service error: " + str(e), 500)

#     return reservation_info_list

def get_reported_issue():
    try:
        issue_reports = get_issue_report_by_filter()
        issue_report_list = []
        def get_dict(issue_report):
            userId = issue_report.userId
            user = get_user_by_id(userId)
            issue_report_data = {
                "issueId": issue_report.reportId,
                "userName": user.name,
                "issue": issue_report.description,
                "date": get_date_time(str(issue_report.createdAt), origin_format="%Y-%m-%d")[0]
            }
            issue_report_list.append(issue_report_data)
        for issue_report in issue_reports:
            if issue_report.isDeleted == False:
                get_dict(issue_report)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)

    return issue_report_list

def delete_reported_issue(issue_id):
    try:
        delete_issue_report(issue_id)
    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def admin_report_analysis():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Reserved)
        classroom_data = get_all_classrooms()  # list of all classroom objects
        classroom_data = [room for room in classroom_data if not room.isDeleted]  # filter out deleted classrooms
        classroom_data = sorted(classroom_data, key=lambda x: x.classroomId)  # sort by classroomId
        classroom_data = {room.classroomId: room for room in classroom_data}  # convert to dictionary for easy access
        time_map = list(slot_time_map.keys())  # Get time slots as a list
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=7)

        # Initialize report: a dictionary for each classroom with 7 days and time slots
        report = {
            room_id: [[0] * len(time_map) for _ in range(7)]  # 7 days x time slots
            for room_id in classroom_data
        }

        # Populate the report with reservation data
        for reservation in reservations:
            classroom_id = reservation.classroomId
            start_time = reservation.startTime
            # end_time = reservation.endTime
            time_slot_start = get_time_slot(str(start_time))
            # time_slot_end = get_time_slot(str(end_time))
            date = get_date_time(str(start_time))[0]
            date = datetime.strptime(date, "%Y-%m-%d").date()

            if date < seven_days_ago or date > today:
                continue

            # Calculate the day index (0 = seven_days_ago, 6 = today)
            day_index = (date - seven_days_ago).days
            print(classroom_id)
            print(day_index)
            print(time_slot_start)
            report[classroom_id][day_index - 1][time_slot_start] += 1

        # Prepare separateData
        separate_data = []
        joint_matrix = [[0] * len(time_map) for _ in range(7)]  # Initialize joint matrix

        for room_id, usage_data in report.items():
            room_name = classroom_data[room_id].classroomName
            total_usage = round(sum(sum(day) for day in usage_data) / 0.7, 2)

            # Add to separate data
            separate_data.append({
                "roomName": room_name,
                "usage": str(total_usage)  # Convert usage to string as per the requirement
            })

            # Update joint matrix
            for day in range(7):
                for time_slot in range(len(time_map)):
                    joint_matrix[day][time_slot] += usage_data[day][time_slot]

        # Prepare jointData
        joint_data = {
            "dates": [(seven_days_ago + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)],
            "matrix": joint_matrix
        }

        # Generate PDF with the matrix table and separate data
        def generate_pdf(joint_data, separate_data, filename):
            pdf = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Add title
            elements.append(Paragraph("Admin Report Analysis", styles["Title"]))

            # Add separateData section
            elements.append(Paragraph("Separate Data", styles["Heading2"]))
            separate_table_data = [["Room Name", "Usage"]]
            for data in separate_data:
                separate_table_data.append([data["roomName"], data["usage"] + "%"])

            separate_table = Table(separate_table_data)
            separate_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header background
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center align all cells
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Header font
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Header padding
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Body background
                ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Grid lines
            ]))
            elements.append(separate_table)

            # Add jointData section
            elements.append(Paragraph("Joint Data", styles["Heading2"]))
            joint_table_data = [["Date/Time"] + time_map]  # Header row
            for i, date in enumerate(joint_data["dates"]):
                joint_table_data.append([date] + joint_data["matrix"][i])  # Add each row

            joint_table = Table(joint_table_data)
            joint_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header background
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center align all cells
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Header font
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Header padding
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Body background
                ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Grid lines
            ]))
            elements.append(joint_table)
            pdf.build(elements)

        # Save the PDF
        pdf_filename = "report.pdf"
        generate_pdf(joint_data, separate_data, pdf_filename)

        return {
            "separateData": separate_data,
            "jointData": joint_data
        }

    except Exception as e:
        raise BusinessError("Service error: " + str(e), 500)