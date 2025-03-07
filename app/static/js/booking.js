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
        getFilteredClassrooms();
        filterModal.style.display = 'none';
    });

    getAllClassrooms();
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

    const apiUrl = '/auth/register';
    const userData = {};

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    const Data = await response.json();

    fetch("http://127.0.0.1:5000/classroom/filter", requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.code === 200) {
                roomList.innerHTML = '';
                result.data.forEach(classroom => {
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
            } else {
                console.log(`Error: ${result.message}`);
            }
        })
        .catch(error => console.log('error', error));
}

function getFilteredClassrooms() {
    const capacityMin = document.getElementById('capacity-min').value;
    const capacityMax = document.getElementById('capacity-max').value;
    const daysOfWeek = Array.from(document.querySelectorAll('input[name="days"]:checked')).map(checkbox => parseInt(checkbox.value));
    const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => parseInt(checkbox.value));
    const roomList = document.getElementById('room-list');

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "capacity_min": capacityMin.parseInt(),
        "capacity_max": capacityMax.parseInt(),
        "date/time": daysOfWeek,
        "equipment": equipment
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/classroom/filter", requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.code === 200) {
                roomList.innerHTML = '';
                result.data.forEach(classroom => {
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
            } else {
                console.log(`Error: ${result.message}`);
            }
        })
        .catch(error => console.log('error', error));
}

function bookClassroom(roomId) {
    const timePeriod = Array.from(document.querySelectorAll('input[name="time-period"]:checked')).map(checkbox => parseInt(checkbox.value));
    const date = document.getElementById('booking-date').value;

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "room_id": parseInt(roomId),
        "time_period": timePeriod,
        "date": date
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/booking/new", requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.code === 200) {
                console.log('Booking successful');
                alert("Booking successful");
            } else {
                console.log(`Error: ${result.message}`);  // TODO
            }
        })
        .catch(error => console.log('error', error));
}

function getEquipmentType() {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/equipment", requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.code === 200) {
                result.data.forEach(equipment => {
                    console.log(`Equipment ID: ${equipment.equipmentId}`);
                    console.log(`Equipment Name: ${equipment.equipmentName}`);
                });
                const equipmentContainer = document.getElementById('equipment');
                equipmentContainer.innerHTML = '';

                result.data.forEach(equipment => {
                    const label = document.createElement('label');
                    label.className = 'date_label';
                    label.innerHTML = `<input type="checkbox" class="ui-checkbox" name="equipment" value="${equipment.equipmentId}"> ${equipment.equipmentName}`;
                    equipmentContainer.appendChild(label);
                });
            } else {
                console.log(`Error: ${result.message}`);
            }
        })
        .catch(error => console.log('error', error));
}
