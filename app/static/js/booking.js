var rooms;

document.addEventListener('DOMContentLoaded', async function () {
    const filterBtn = document.getElementById('filter-btn');
    const filterModal = document.getElementById('filter-modal');
    const applyFilterBtn = document.getElementById('apply-filter');
    const dateInput = document.getElementById('booking-date');

    filterBtn.addEventListener('click', async function () {
        filterModal.style.display = 'flex';
        const equipments = await getEquipmentType();
        const equipments_container = document.getElementById('equipment')
        equipments_container.innerHTML = '';

        equipments.forEach(equipment => {
            const label = document.createElement('label');
            label.className = 'date_label';

            label.innerHTML = `<input type="checkbox" class="ui-checkbox" name="equipment" value="${equipment.equipmentId}">${equipment.equipmentName}`
            equipments_container.appendChild(label)
        })

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
    // set default date to today
    await getTodayClassrooms(dateInput);

    viewRooms();
});

document.addEventListener('DOMContentLoaded', () => {
    const bookingModal = document.getElementById('booking-modal');
    const confirmBookingButton = document.getElementById('confirm-booking');

    confirmBookingButton.addEventListener('click', () => {
        const roomId = bookingModal.getAttribute('data-room-id');
        handleBookings(roomId);
        bookingModal.style.display = 'none';
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', (event) => {
        if (event.target === bookingModal) {
            bookingModal.style.display = 'none';
        }
    });
});

async function getTodayClassrooms(dateInput) {
    const date = new Date().toISOString().split('T')[0];
    dateInput.value = date;
    rooms = await getFilteredClassrooms("", "", date, []);
}

async function getFilteredClassrooms(capacity_min, capacity_max, date, equipment) {
    const apiUrl = '/classroom/filter';
    const userData = {
        "capacity_min": capacity_min,
        "capacity_max": capacity_max,
        "date": date,
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
        'room_id': room_id,
        'date':date,
        'time_period': time_period
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
    const apiUrl = '/classroom/equipment';
    // const userData = {};

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        // body: JSON.stringify(userData),
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
    const roomList = document.getElementById('room-list');

    if (rooms.length > 0) {
        roomList.innerHTML = '';
        rooms.forEach(classroom => {
            const room = document.createElement('div')
            room.className = 'room-card'
            room.innerHTML = `
                            <h3>${classroom.classroomName}</h3>
                            <p>Capacity: ${classroom.capacity}</p>
                            <p>Equipment: ${classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constrain: ${classroom.isRestricted ? classroom.constrain : 'None'}</p>
                            <button class="action-btn book-now-btn" data-room-id="${classroom.classroomId}" data-room-available-time="${classroom.timePeriod}">Book Now</button>
                    `;
            roomList.appendChild(room);
        });

        // Add event listeners to the newly created buttons
        const bookNowButtons = document.querySelectorAll('.book-now-btn');
        bookNowButtons.forEach(button => {
            button.addEventListener('click', () => {
                const bookingModal = document.getElementById('booking-modal');
                bookingModal.style.display = 'flex';
                bookingModal.setAttribute('data-room-id', button.getAttribute('data-room-id'));
                bookingModal.setAttribute('data-room-available-time', button.getAttribute('data-room-available-time'));
                document.querySelectorAll('input[name="time-period"]').forEach(checkbox => {
                    checkbox.checked = false;
                    checkbox.disabled = !button.getAttribute('data-room-available-time').split(',').includes(checkbox.value);
                });
            });
        });
    }
}

async function handleFilters() {
    const capacity_min = document.getElementById('capacity-min').value;
    const capacity_max = document.getElementById('capacity-max').value;
    const date = document.getElementById('booking-date').value;
    const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => checkbox.value);
    document.getElementById('filter-date').innerText = `Checking Date: ${date}`;
    const rooms = await getFilteredClassrooms(capacity_min, capacity_max, date, equipment);
    const roomList = document.getElementById('room-list');

    if (rooms.length > 0) {
        roomList.innerHTML = '';
        rooms.forEach(classroom => {
            const room = document.createElement('div')
            room.className = 'room-card'
            room.innerHTML = `
                            <h3>${classroom.classroomName}</h3>
                            <p>Capacity: ${classroom.capacity}</p>
                            <p>Equipment: ${classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constrain: ${classroom.isRestricted ? classroom.constrain : 'None'}</p>
                            <button class="action-btn book-now-btn" data-room-id="${classroom.classroomId}" data-room-available-time="${classroom.timePeriod}">Book Now</button>
                    `;
            roomList.appendChild(room);
        });

        // Add event listeners to the newly created buttons
        const bookNowButtons = document.querySelectorAll('.book-now-btn');
        bookNowButtons.forEach(button => {
            button.addEventListener('click', () => {
                const bookingModal = document.getElementById('booking-modal');
                bookingModal.style.display = 'flex';
                bookingModal.setAttribute('data-room-id', button.getAttribute('data-room-id'));
                bookingModal.setAttribute('data-room-available-time', button.getAttribute('data-room-available-time'));
                document.querySelectorAll('input[name="time-period"]').forEach(checkbox => {
                    checkbox.checked = false;
                    checkbox.disabled = !button.getAttribute('data-room-available-time').split(',').includes(checkbox.value);
                });
            });
        });
    }
}

async function handleBookings(room_id) {
    const date = document.getElementById('booking-date').value;
    const time_period = Array.from(document.querySelectorAll('input[name="time-period"]:checked')).map(checkbox => parseInt(checkbox.value));
    await bookClassroom(room_id, date, time_period);
}