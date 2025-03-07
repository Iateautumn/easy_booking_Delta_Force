document.addEventListener('DOMContentLoaded', function () {
    const filterBtn = document.getElementById('filter-btn');
    const filterModal = document.getElementById('filter-modal');
    const applyFilterBtn = document.getElementById('apply-filter');

    filterBtn.addEventListener('click', function () {
        filterModal.style.display = 'flex';
        getEquipmentType();
    });

    filterModal.addEventListener('click', function (event) {
        if (event.target === filterModal) {
            filterModal.style.display = 'none';
        }
    });

    applyFilterBtn.addEventListener('click', function () {
        handleFilters();
        filterModal.style.display = 'none';
    });

    viewRooms();
});

document.addEventListener('DOMContentLoaded', () => {
    const bookingModal = document.getElementById('booking-modal');
    const bookNowButtons = document.querySelectorAll('.action-btn');
    const confirmBookingButton = document.getElementById('confirm-booking');

    bookNowButtons.forEach(button => {
        button.addEventListener('click', () => {
            bookingModal.style.display = 'flex';
            bookingModal.setAttribute('data-room-id', button.getAttribute('data-room-id'));
        });
    });

    confirmBookingButton.addEventListener('click', () => {
        const roomId = bookingModal.getAttribute('data-room-id');
        bookClassroom(roomId);
        bookingModal.style.display = 'none';
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', (event) => {
        if (event.target === bookingModal) {
            bookingModal.style.display = 'none';
        }
    });
});

async function getAllClassrooms() {
    const apiUrl = '/classroom/filter';
    const userData = {};

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
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
    }
    else {
        alert('Error, Network Error');
        return [];
    }
}

async function getFilteredClassrooms(capacity_min, capacity_max, date, equipment) {
    const apiUrl = '/classroom/filter';
    const userData = {
        "capacity_min": capacity_min,
        "capacity_max": capacity_max,
        "date/time": date,
        "equipment": equipment
    };

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
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
    }
    else {
        alert('Error, Network Error');
        return [];
    }

}

async function bookClassroom(room_id, date, time_period) {
    const apiUrl = '/booking/new';
    const userData = {
        room_id,
        date,
        time_period
    };

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const Data = await response.json();

    if (Data) {
        switch (Data.code) {
            case 200:
                alert('Booking successful');
                break;
            case 409:
                alert('Booking failed, Room already booked');
                break;
            default:
                alert(`Error, (${Data.message})`);
        }
    }
    else {
        alert('Error, Network Error');
    }

}

async function getEquipmentType() {
    const apiUrl = '/equipment';
    const userData = {};

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
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


async function viewRooms() {
    const rooms = await getAllClassrooms();
    const roomList = document.getElementById('room-list');

    if (rooms.length > 0) {
        roomList.innerHTML = '';
        rooms.forEach(classroom => {
            const li = document.createElement('li');
            li.innerHTML = `
                        <div class="room-info">
                            <h3>${classroom.classroomName}</h3>
                            <p>Capacity: ${classroom.capacity}</p>
                            <p>Equipment: ${classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constrain: ${classroom.isRestricted ? classroom.constrain : 'None'}</p>
                        </div>
                        <button class="action-btn" data-room-id="${classroom.classroomId}">Book Now</button>
                    `;
            roomList.appendChild(li);
        });

    }
}

async function handleFilters() {
    const capacity_min = document.getElementById('capacity-min').value;
    const capacity_max = document.getElementById('capacity-max').value;
    const date = Array.from(document.querySelectorAll('input[name="days"]:checked')).map(checkbox => parseInt(checkbox.value));
    const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => checkbox.value);

    const rooms = await getFilteredClassrooms(capacity_min, capacity_max, date, equipment);
    const roomList = document.getElementById('room-list');

    if (rooms.length > 0) {
        roomList.innerHTML = '';
        rooms.forEach(classroom => {
            const li = document.createElement('li');
            li.innerHTML = `
                        <div class="room-info">
                            <h3>${classroom.classroomName}</h3>
                            <p>Capacity: ${classroom.capacity}</p>
                            <p>Equipment: ${classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constrain: ${classroom.isRestricted ? classroom.constrain : 'None'}</p>
                        </div>
                        <button class="action-btn" data-room-id="${classroom.classroomId}">Book Now</button>
                    `;
            roomList.appendChild(li);
        });
    }
}

async function handleBookings(room_id) {
    const date = document.getElementById('date').value;
    const time_period = document.getElementById('time-period').value;
    await bookClassroom(room_id, date, time_period);
}


