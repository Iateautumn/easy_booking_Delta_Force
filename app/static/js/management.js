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