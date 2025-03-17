document.addEventListener('DOMContentLoaded', async function () {
    const addRoomModal = document.querySelector('#add-room-modal');
    const modifyRoomModal = document.querySelector('#modify-room-modal');
    const addRoomBtn = document.querySelector('#add-room-btn');
    const applyAddRoomBtn = document.querySelector('#apply-add-room-btn');
    const applyModifyBtn = document.querySelector('#apply-modify-room-btn');

    addRoomBtn.addEventListener('click', async function () {

        const equipments = await getEquipmentType();
        const equipments_container = document.getElementById('add-room-equipment')
        equipments_container.innerHTML = '';

        equipments.forEach(equipment => {
            const label = document.createElement('label');
            label.className = 'date_label';

            label.innerHTML = `<input type="checkbox" class="ui-checkbox" name="add-room-equipment" value="${equipment.equipmentId}">${equipment.equipmentName}`
            equipments_container.appendChild(label)
        })
        addRoomModal.style.display = 'flex';
    });

    applyAddRoomBtn.addEventListener('click', async function () {
        const classroom_name = document.querySelector('#input-add-room-name').value;
        const capacity = document.querySelector('#add-room-capacity').value;
        const equipment = Array.from(document.querySelectorAll('input[name="add-room-equipment"]:checked')).map(checkbox => checkbox.value);
        const new_equipment_str = document.querySelector('#add-room-new-equipment').value;
        const constrain = document.querySelector('#input-add-room-constrain').value;
        const new_equipment = new_equipment_str.split(',').map(equipment => equipment.trim());

        const result = await adminAddRoom(classroom_name, capacity, equipment, new_equipment, constrain);

        if (result) {
            alert('Add successful');
            viewAllRooms();
        } else {
            alert('Add failed');
        }
        addRoomModal.style.display = 'none';
    });

    applyModifyBtn.addEventListener('click', async function () {
        const classroom_id = modifyRoomModal.getAttribute('room-id');
        const classroom_name = document.querySelector('#input-modify-room-name').value;
        const capacity = document.querySelector('#modify-room-capacity').value;
        const equipment = Array.from(document.querySelectorAll('input[name="modify-room-equipment"]:checked')).map(checkbox => checkbox.value);
        const new_equipment_str = document.querySelector('#modify-room-new-equipment').value;
        const constrain = document.querySelector('#input-modify-room-constrain').value;
        const new_equipment = new_equipment_str.split(',').map(equipment => equipment.trim());

        const result = await adminModifyRoomInfo(classroom_id, classroom_name, capacity, equipment, new_equipment, constrain);

        if (result) {
            alert('Modify successful');
            viewAllRooms();
        } else {
            alert('Modify failed');
        }
        modifyRoomModal.style.display = 'none';
    });

    addRoomModal.addEventListener('click', function (event) {
        if (event.target === addRoomModal) {
            addRoomModal.style.display = 'none';
        }
    });

    modifyRoomModal.addEventListener('click', function (event) {
        if (event.target === modifyRoomModal) {
            modifyRoomModal.style.display = 'none';
        }
    });


    await viewAllRooms();
});

async function viewAllRooms() {
    const rooms = await adminGetAllRoomsInfo();
    const roomList = document.querySelector('.room-list');

    if (rooms.length > 0) {
        roomList.innerHTML = '';
        rooms.forEach(room => {
            const eqs = room.equipments;
            let equipment_display = '';
            let equipment_id = '';
            if (eqs.length > 0) {
                equipment_display = eqs.map(eq => eq.equipmentName).join(', ');
                equipment_id = eqs.map(eq => eq.equipmentId).join(', ');
            }
            const roomCard = document.createElement('div');
            roomCard.classList.add('room-card');
            roomCard.innerHTML = `
                <h3>${room.classroomName}</h3>
                <p>Capacity: ${room.capacity}</p>
                <p>Equipment: ${equipment_display}</p>
                <p>Constrain: ${room.constrain}</p>
                <button class="action-btn" id="modify-room" equipment-id="${equipment_id}">Modify</button>
                <button class="action-btn" id="delete-room">Delete</button>
            `;
            roomList.appendChild(roomCard);
        });

        const modifyRoomBtns = document.querySelectorAll('#modify-room');
        const deleteRoomBtns = document.querySelectorAll('#delete-room');

        modifyRoomBtns.forEach((btn, index) => {
            btn.addEventListener('click', async () => {
                const room = rooms[index];
                document.querySelector('#input-modify-room-name').value = room.classroomName;
                document.querySelector('#modify-room-capacity').value = room.capacity;
                document.querySelector('#modify-room-new-equipment').value = '';
                document.querySelector('#input-modify-room-constrain').value = room.constrain;
                document.querySelector('#modify-room-modal').style.display = 'flex';
                document.querySelector('#modify-room-modal').setAttribute('room-id', room.classroomId);

                const equipments = await getEquipmentType();
                const equipments_container = document.getElementById('modify-room-equipment')
                equipments_container.innerHTML = '';

                equipments.forEach(equipment => {
                    const label = document.createElement('label');
                    label.className = 'date_label';

                    label.innerHTML = `<input type="checkbox" class="ui-checkbox" name="modify-room-equipment" value="${equipment.equipmentId}">${equipment.equipmentName}`
                    equipments_container.appendChild(label)
                })
                btn.getAttribute('equipment-id').split(',').forEach(equipment_id => {
                    document.querySelector(`input[name="modify-room-equipment"][value="${equipment_id.trim()}"]`).checked = true;
                });
                // equipment_ids.forEach(equipment_id => {
                //     document.querySelector(`input[name="modify-room-equipment"][value="${equipment_id}"]`).checked = true;
                // });
            });
        });

        deleteRoomBtns.forEach((btn, index) => {
            btn.addEventListener('click', async () => {
                const room = rooms[index];
                const result = await adminDeleteRoom(room.classroomId);

                if (result) {
                    alert('Delete successful');
                    viewAllRooms();
                } else {
                    alert('Delete failed');
                }
            });
        });
    }
}

async function adminGetAllRoomsInfo() {
    const apiUrl = '/admin/classroom/all';
    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    const data = await response.json();

    if (data) {
        switch (data.code) {
            case 200:
                return Array.isArray(data.data) ? data.data : [];
            default:
                alert(`Error, (${data.message})`);
                return [];
        }
    }
}

async function adminAddRoom(classroom_name, capacity, equipment, new_equipment, constrain) {
    const apiUrl = '/admin/classroom/add';
    const userData = {
        "classroom_name": classroom_name,
        "capacity": capacity,
        "equipment": equipment,
        "new_equipment": new_equipment,
        "constrain": constrain
    }

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (data) {
        switch (data.code) {
            case 200:
                return true;
            default:
                alert(`Error, (${data.message})`);
                return false;
        }
    } else {
        alert('Error, Network Error');
        return false;
    }
}

async function adminDeleteRoom(classroom_id) {
    const apiUrl = '/admin/classroom/remove';
    const userData = {
        "classroom_id": classroom_id
    }

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (data) {
        switch (data.code) {
            case 200:
                return true;
            default:
                alert(`Error, (${data.message})`);
                return false;
        }
    } else {
        alert('Error, Network Error');
        return false;
    }

}

async function adminModifyRoomInfo(classroom_id, classroom_name, capacity, equipment, new_equipment, constrain) {
    const apiUrl = '/admin/classroom/modify';
    const userData = {
        "classroom_id": classroom_id,
        "classroom_name": classroom_name,
        "capacity": capacity,
        "equipment": equipment,
        "new_equipment": new_equipment,
        "constrain": constrain
    }

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (data) {
        switch (data.code) {
            case 200:
                return true;
            default:
                alert(`Error, (${data.message})`);
                return false;
        }
    } else {
        alert('Error, Network Error');
        return false;
    }

}

async function getEquipmentType() {
    const apiUrl = '/classroom/equipment';

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    const Data = await response.json();

    if (Data) {
        switch (Data.code) {
            case 200:
                return Array.isArray(Data.data) ? Data.data : [];
            default:
                alert(`Error, (${Data.message})`);
                return [];
        }
    } else {
        alert('Error, Network Error');
        return [];
    }
}