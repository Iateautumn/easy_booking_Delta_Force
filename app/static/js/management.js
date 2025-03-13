document.addEventListener('DOMContentLoaded', async function() {
    const addRoomModal = document.querySelector('#add-room-modal');
    const modifyRoomModal = document.querySelector('#modify-room-modal');
    const addRoomBtn = document.querySelector('#add-room-btn');
    const applyAddRoomBtn = document.querySelector('#apply-add-room-btn');
    const applyModifyBtn = document.querySelector('#apply-modify-room-btn');

    addRoomBtn.addEventListener('click', function() {
        addRoomModal.style.display = 'flex';
    });

    applyAddRoomBtn.addEventListener('click', async function() {
        const classroom_name = document.querySelector('#input-add-room-name').value;
        const capacity = document.querySelector('#add-room-capacity').value;
        const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => checkbox.value);
        const new_equipment_str = document.querySelector('#add-room-new-equipment').value;
        const constrain = document.querySelector('#input-add-room-constrain').value;
        const new_equipment = new_equipment_str.split(',').map(equipment => equipment.trim());

        await adminAddRoom(classroom_name, capacity, equipment, new_equipment, constrain);

        addRoomModal.style.display = 'none';
    });

    applyModifyBtn.addEventListener('click', async function() {
        const classroom_name = document.querySelector('#input-modify-room-name').value;
        const capacity = document.querySelector('#modify-room-capacity').value;
        const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => checkbox.value);
        const new_equipment_str = document.querySelector('#modify-room-new-equipment').value;
        const constrain = document.querySelector('#input-modify-room-constrain').value;
        const new_equipment = new_equipment_str.split(',').map(equipment => equipment.trim());

        await adminModifyRoomInfo(classroom_name, capacity, equipment, new_equipment, constrain);

        modifyRoomModal.style.display = 'none';
    });

    addRoomModal.addEventListener('click', function(event) {
        if (event.target === addRoomModal) {
            addRoomModal.style.display = 'none';
        }
    });

    modifyRoomModal.addEventListener('click', function(event) {
        if (event.target === modifyRoomModal) {
            modifyRoomModal.style.display = 'none';
        }
    });

    const rooms = adminGetAllRoomsInfo();
    const roomList = document.querySelector('.room-list');

    if (rooms.length > 0) {
        roomList.innerHTML = '';
        rooms.forEach(room => {
            const roomCard = document.createElement('div');
            roomCard.classList.add('room-card');
            roomCard.innerHTML = `
                <h3>${room.classroom_name}</h3>
                <p>Capacity: ${room.capacity}</p>
                <p>Equipment: ${room.equipment}</p>
                <p>Constrain: ${room.constrain}</p>
                <button class="action-btn" id="modify-room">Modify</button>
                <button class="action-btn" id="delete-room">Delete</button>
            `;
            roomList.appendChild(roomCard);
        });

        const modifyRoomBtns = document.querySelectorAll('#modify-room');
        const deleteRoomBtns = document.querySelectorAll('#delete-room');

        modifyRoomBtns.forEach((btn, index) => {
            btn.addEventListener('click', () => {
                const room = rooms[index];
                document.querySelector('#input-modify-room-name').value = room.classroom_name;
                document.querySelector('#modify-room-capacity').value = room.capacity;
                const equipment = room.equipment.split(',').map(equipment => equipment.trim());
                equipment.forEach(equipment => {
                    document.querySelector(`input[name="equipment"][value="${equipment}"]`).checked = true;
                });
                document.querySelector('#modify-room-new-equipment').value = '';
                document.querySelector('#input-modify-room-constrain').value = room.constrain;
                document.querySelector('#modify-room-modal').style.display = 'flex';
            });
        });

        deleteRoomBtns.forEach((btn, index) => {
            btn.addEventListener('click', async () => {
                const room = rooms[index];
                await adminDeleteRoom(room.classroom_id);
            });
        });
    }
});

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
                alert('Add successful');
                break;
            default:
                alert(`Error, (${data.message})`);
        }
    }
    else {
        alert('Error, Network Error');
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
                alert('Delete successful');
                break;
            default:
                alert(`Error, (${data.message})`);
        }
    }
    else {
        alert('Error, Network Error');
    }
    
}

async function adminModifyRoomInfo(classroom_name, capacity, equipment, new_equipment, constrain) {
    const apiUrl = '/admin/classroom/modify';
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
                alert('Modify successful');
                break;
            default:
                alert(`Error, (${data.message})`);
        }
    }
    else {
        alert('Error, Network Error');
    }
    
}