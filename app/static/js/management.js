document.addEventListener('DOMContentLoaded', async function() {
    const addRoomModal = document.querySelector('#add-room-modal');
    const modifyRoomModal = document.querySelector('#modify-room-modal');
    const addRoomBtn = document.querySelector('#add-room-btn');
    const applyAddRoomBtn = document.querySelector('#apply-add-room-btn');
    const modifyBtn = document.querySelector('#modify-room-btn');
    const applyModifyBtn = document.querySelector('#apply-modify-room-btn');

    addRoomBtn.addEventListener('click', function() {
        addRoomModal.style.display = 'flex';
    });

    applyAddRoomBtn.addEventListener('click', function() {
        // TODO
        addRoomModal.style.display = 'none';
    });

    modifyBtn.addEventListener('click', function() {
        modifyRoomModal.style.display = 'flex';
    });

    applyModifyBtn.addEventListener('click', function() {
        // TODO
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

    viewBookings();
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

async function adminAddRoom(classroom_id, classroom_name, capacity, equipment, new_equipment, constrain) {
    const apiUrl = '/admin/classroom/add';
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

async function addminDeleteRoom(classroom_id) {
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