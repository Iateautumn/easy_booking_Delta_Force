var rooms;
var capacity_min = "";
var capacity_max = "";
var date;
var equipment = [];

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

        console.log(equipment);
        

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
        const loading_item = document.getElementById('loading-item');
        loading_item.style.display = 'flex';
        document.getElementById('loading-hint').innerText = 'Booking...';

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

document.addEventListener('DOMContentLoaded', () => {

    const reportBtn = document.getElementById('report-btn');
    const reportModal = document.getElementById('report-modal');
    const applyReportBtn = document.getElementById('apply-report');


    reportBtn.addEventListener('click', function () {
        reportModal.style.display = 'flex';
    });

    reportModal.addEventListener('click', function (event) {
        if (event.target === reportModal) {
            reportModal.style.display = 'none';
        }
    });

    applyReportBtn.addEventListener('click', async function () {
        handleReport();
        reportModal.style.display = 'none';
    });

})


async function getTodayClassrooms(dateInput) {
    const date = new Date().toISOString().split('T')[0];
    dateInput.value = date;
    rooms = await getFilteredClassrooms("", "", date, [], 2);
    document.getElementById('filter-date').innerText = `Checking Date: ${date}`;
}

async function getFilteredClassrooms(capacity_min, capacity_max, date, equipment, issue) {
    const apiUrl = '/classroom/filter';
    const userData = {
        "capacity_min": capacity_min,
        "capacity_max": capacity_max,
        "date": date,
        "equipment": equipment
    };

    if (issue != 2 && issue != "") {
        userData.issue = issue == 1 ? true : false;
    }

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

async function bookClassroom(room_id, date, time_period) {
    const apiUrl = '/booking/new';
    const userData = {

        'room_id': room_id,
        'date': date,
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
                return true;
            case 409:
                alert('Booking failed, Room already booked');
                return false;
            default:
                alert(`Error, (${Data.message})`);
                return false;
        }
    } else {
        alert('Error, Network Error');
        return false;
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

async function userReportIssue(issue) {
    const apiUrl = '/user/classroom/issue/report';
    const userData = {
        "issue": issue
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
                return true;
            default:
                alert(`Error, (${Data.message})`);
                return false;
        }
    } else {
        alert('Error, Network Error');
        return false;
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
                            <p>Equipment: ${(!classroom.equipments || classroom.equipments.length == 0) ? 'None' : classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constraint: ${(!classroom.constrain || classroom.constrain == '') ? 'None' : classroom.constrain}</p>
                            ${classroom.issue ? '<p style="color: #d20000">Issue: ' + classroom.issue + '</p>' : ''}
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
    else{
        roomList.innerHTML = 'No Rooms Found';
    }
    const loading_item = document.getElementById('loading-item');
    loading_item.style.display = 'none';
}


async function handleFilters() {
    capacity_min = document.getElementById('capacity-min').value;
    capacity_max = document.getElementById('capacity-max').value;
    date = document.getElementById('booking-date').value;
    equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => checkbox.value);
    document.getElementById('filter-date').innerText = `Checking Date: ${date}`;
    issue = document.getElementById('issue-select').value;

    const roomList = document.getElementById('room-list');
    roomList.innerHTML = '';
    const loading_item = document.getElementById('loading-item');
    loading_item.style.display = 'flex';
    const rooms = await getFilteredClassrooms(capacity_min, capacity_max, date, equipment,issue);
    

    if (rooms.length > 0) {
        rooms.forEach(classroom => {
            const room = document.createElement('div')
            room.className = 'room-card'
            room.innerHTML = `
                            <h3>${classroom.classroomName}</h3>
                            <p>Capacity: ${classroom.capacity}</p>
                            <p>Equipment: ${(!classroom.equipments || classroom.equipments.length == 0) ? 'None' : classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constraint: ${(!classroom.constrain || classroom.constrain == '') ? 'None' : classroom.constrain}</p>
                            ${classroom.issue ? '<p style="color: #d20000">Issue: ' + classroom.issue + '</p>' : ''}
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
    else{
        roomList.innerHTML = 'No Rooms Found';
    }
    loading_item.style.display = 'none';
}

async function handleBookings(room_id) {
    const date = document.getElementById('booking-date').value;
    const time_period = Array.from(document.querySelectorAll('input[name="time-period"]:checked')).map(checkbox => parseInt(checkbox.value));
    const result = await bookClassroom(room_id, date, time_period);

    const roomList = document.getElementById('room-list');
    roomList.innerHTML = '';
    document.getElementById('loading-hint').innerText = 'Loading Rooms...';
    if (result) {
        alert('Booked');
        rooms = await getFilteredClassrooms(capacity_min, capacity_max, date, equipment);
        viewRooms();
    } else {
        alert('Booking failed');
        document.getElementById('loading-item').style.display = 'none';
        viewRooms();
    }
}

async function handleReport() {
    var issue = document.getElementById('issue').value;
    const result = await userReportIssue(issue);
    if (result) {
        alert('Reported');
        document.getElementById('issue').value = "";
    } else {
        alert('Error, Network Error');
    }
}


