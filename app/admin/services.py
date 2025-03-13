
from app.auth.models import User, get_user_by_id
from app.booking.models import (
Reservation, 
ReservationStatus, 
get_reservation_by_status, 
get_reservation_by_id,
update_reservation)
from app.classroom.models import Classroom, get_classroom_by_id
from app.utils.datetime_utils import slot_time_map, get_time_slot, get_date_time
from app.utils.exceptions import BusinessError

### 这里的user是一个管理员admin，the administrator can approve the booking request for restricted rooms 

### 获取所有未处理的预约请求
def get_reservation_requests():
    try:
        reservations = get_reservation_by_status(ReservationStatus.Pending)
        print(reservations)
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

### 同意预约请求
def approve_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Reserved)

        # reservation.status = ReservationStatus.Approved
        
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
    

### 拒绝预约请求
def reject_reservation(reservationId):
    try:
        reservation = get_reservation_by_id(reservationId)
        userId = reservation.userId
        classroomId = reservation.classroomId
        reservation = update_reservation(reservationId, userId, classroomId, reservation.startTime, reservation.endTime, ReservationStatus.Rejected)
    except Exception as e:
        raise BusinessError("Reservation not found: " + str(e), 404)
         


def add_room(current_user, classroom_name, capacity, equipment_ids=[], constrain=None, is_restricted=False):

    if current_user.status != UserStatus.Admin.value:
        return {"status": "error", "message": "no admin power"}, 403

    try:
        new_classroom = Classroom.add_classroom(
            classroomName=classroom_name,
            capacity=capacity
        )

        if constrain:
            new_classroom.constrain = constrain
        new_classroom.isRestricted = is_restricted
        new_classroom.updatedAt = datetime.now()

        for equip_id in equipment_ids:
            ClassEquipment.add_classequipment(
                classroomId=new_classroom.classroomId,
                equipmentId=equip_id
            )

        db.session.commit()

        return {
            "code": 200,
            "message": "Classroom created successfully",
            "data": [str(new_classroom.classroomId)]
        }

    except db.IntegrityError:
        db.session.rollback()
        return {
            "code": 409,
            "message": "Classroom name already exists",
            "data": []
        }
    except ValueError as ve:
        db.session.rollback()
        return {
            "code": 400,
            "message": str(ve),
            "data": []
        }
    except Exception as e:
        db.session.rollback()
        return {
            "code": 500,
            "message": f"Server error: {str(e)}",
            "data": []
        }


def modify_room(current_user, classroom_id, classroom_name=None, capacity=None,
                equipment_ids=None, constrain=None, is_restricted=None):

    if current_user.status != UserStatus.Admin.value:
        return {"status": "error", "message": "no admin power"}, 403

    try:
        # 基础信息更新
        updated = Classroom.update_classroom(
            classroomId=classroom_id,
            classroomName=classroom_name,
            capacity=capacity
        )

        classroom = Classroom.get_classroom_by_id(classroom_id)

        if constrain is not None:
            classroom.constrain = constrain
        if is_restricted is not None:
            classroom.isRestricted = is_restricted
        classroom.updatedAt = datetime.now()

        if equipment_ids is not None:
            existing_equipments = ClassEquipment.get_classequipment_by_classroom_id(classroom_id)
            for eq in existing_equipments:
                ClassEquipment.delete_classequipment(eq.classEquipmentId)

            for equip_id in equipment_ids:
                ClassEquipment.add_classequipment(
                    classroomId=classroom_id,
                    equipmentId=equip_id
                )

        db.session.commit()
        return {
            "code": 200,
            "message": "Classroom updated successfully",
            "data": [str(classroom_id)]
        }

    except db.IntegrityError:
        db.session.rollback()
        return {
            "code": 409,
            "message": "Classroom name already exists",
            "data": []
        }
    except ValueError as ve:
        db.session.rollback()
        return {
            "code": 400,
            "message": str(ve),
            "data": []
        }
    except Exception as e:
        db.session.rollback()
        return {
            "code": 500,
            "message": f"Server error: {str(e)}",
            "data": []
        }


def delete_room(current_user, classroom_id):
    def delete_room(current_user, request_data):
        if current_user.status != UserStatus.Admin.value:
            return {
                "code": 403,
                "message": "Permission denied",
                "data": []
            }

        try:
            if "classroom_id" not in request_data:
                return {
                    "code": 400,
                    "message": "Missing classroom_id parameter",
                    "data": []
                }

            classroom_id = request_data["classroom_id"]
            classroom = Classroom.get_classroom_by_id(classroom_id)


            if not classroom:
                return {
                    "code": 404,
                    "message": "Classroom not found",
                    "data": []
                }


            if classroom.isDeleted:
                return {
                    "code": 200,
                    "message": "Classroom already deleted",
                    "data": [str(classroom_id)]
                }


            Classroom.delete_classroom(classroom_id)


            equipment_relations = ClassEquipment.get_classequipment_by_classroom_id(classroom_id)
            for relation in equipment_relations:
                ClassEquipment.delete_classequipment(relation.classEquipmentId)

            db.session.commit()

            return {
                "code": 200,
                "message": "Classroom deleted successfully",
                "data": [str(classroom_id)]
            }

        except ValueError as ve:
            db.session.rollback()
            return {
                "code": 400,
                "message": str(ve),
                "data": []
            }
        except Exception as e:
            db.session.rollback()
            return {
                "code": 500,
                "message": f"Server error: {str(e)}",
                "data": []
            }


def get_all_rooms(current_user):
    # 权限验证
    if current_user.status != UserStatus.Admin.value:
        return {"status": "error", "message": "no admin power"}, 403

    try:
        # 获取所有教室（包含软删除的）
        all_classrooms = Classroom.query.options(
            db.joinedload(Classroom.Equipments)
        ).order_by(Classroom.classroomId).all()

        # 构建响应数据
        classroom_data = []
        for room in all_classrooms:
            # 处理设备信息（过滤已删除设备）
            valid_equipments = [
                {"id": eq.equipmentId, "name": eq.equipmentName}
                for eq in room.Equipments if not eq.isDeleted
            ]

            classroom_data.append({
                "id": room.classroomId,
                "name": room.classroomName,
                "capacity": room.capacity,
                "constrain": room.constrain,
                "is_restricted": room.isRestricted,
                "status": "active" if not room.isDeleted else "deleted",
                "equipments": valid_equipments,
                "created_at": room.createdAt.isoformat() if room.createdAt else None,
                "updated_at": room.updatedAt.isoformat() if room.updatedAt else None
            })

        return {
            "status": "success",
            "data": {
                "total": len(classroom_data),
                "classrooms": classroom_data
            }
        }, 200

    except Exception as e:
        return {"status": "error", "message": f" no found in database asset: {str(e)}"}, 500

