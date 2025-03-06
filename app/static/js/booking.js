document.addEventListener('DOMContentLoaded', function () {
    const filterBtn = document.getElementById('filter-btn');
    const filterModal = document.getElementById('filter-modal');
    const capacitySlider = document.getElementById('capacity');
    const capacityValue = document.getElementById('capacity-value');
    const applyFilterBtn = document.getElementById('apply-filter');

    filterBtn.addEventListener('click', function () {
        filterModal.style.display = 'flex';
    });

    filterModal.addEventListener('click', function (event) {
        if (event.target === filterModal) {
            filterModal.style.display = 'none';
        }
    });

    applyFilterBtn.addEventListener('click', function () {
        // Add your filter logic here
        filterModal.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const bookingModal = document.getElementById('booking-modal');
    const bookNowButtons = document.querySelectorAll('.action-btn');
    const confirmBookingButton = document.getElementById('confirm-booking');

    bookNowButtons.forEach(button => {
        button.addEventListener('click', () => {
            bookingModal.style.display = 'flex';
        });
    });

    confirmBookingButton.addEventListener('click', () => {
        // Add your booking confirmation logic here
        bookingModal.style.display = 'none';
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', (event) => {
        if (event.target === bookingModal) {
            bookingModal.style.display = 'none';
        }
    });
});

// use /classroom/filter GET to get all classrooms
function getAllClassrooms() {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    const roomList = document.getElementById('room-list');

    var raw = JSON.stringify({});

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/classroom/filter", requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.code === 200) {
                result.data.forEach(classroom => {
                    console.log(`Classroom ID: ${classroom.classroomId}`);
                    console.log(`Classroom Name: ${classroom.classroomName}`);
                    console.log(`Capacity: ${classroom.capacity}`);
                    console.log(`Is Deleted: ${classroom.isDeleted}`);
                    console.log(`Created At: ${classroom.createdAt}`);
                    console.log(`Updated At: ${classroom.updatedAt}`);
                    classroom.equipments.forEach(equipment => {
                        console.log(`  Equipment ID: ${equipment.equipmentId}`);
                        console.log(`  Equipment Name: ${equipment.equipmentName}`);
                        console.log(`  Created At: ${equipment.createAt}`);
                        console.log(`  Updated At: ${equipment.updateAt}`);
                        console.log(`  Is Deleted: ${equipment.idDeleted}`);
                    });
                });
                roomList.innerHTML = '';
                result.data.forEach(classroom => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <div class="room-info">
                            <h3>${classroom.classroomName}</h3>
                            <p>Capacity: ${classroom.capacity}</p>
                            <p>Equipment: ${classroom.equipments.map(equipment => equipment.equipmentName).join(', ')}</p>
                            <p>Constrain: </p>
                        </div>
                        <button class="action-btn">Book Now</button>
                    `;
                    roomList.appendChild(li);
                });
            } else {
                console.log(`Error: ${result.message}`);
            }
        })
        .catch(error => console.log('error', error));
    // TODO
}

function getFilteredClassrooms() {
    const capacityMin = document.getElementById('capacity-min').value;
    const capacityMax = document.getElementById('capacity-max').value;
    const daysOfWeek = Array.from(document.querySelectorAll('input[name="days"]:checked')).map(checkbox => parseInt(checkbox.value));
    const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(checkbox => parseInt(checkbox.value));

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
                result.data.forEach(classroom => {
                    console.log(`Classroom ID: ${classroom.classroomId}`);
                    console.log(`Classroom Name: ${classroom.classroomName}`);
                    console.log(`Capacity: ${classroom.capacity}`);
                    console.log(`Is Deleted: ${classroom.isDeleted}`);
                    console.log(`Created At: ${classroom.createdAt}`);
                    console.log(`Updated At: ${classroom.updatedAt}`);
                    classroom.equipments.forEach(equipment => {
                        console.log(`  Equipment ID: ${equipment.equipmentId}`);
                        console.log(`  Equipment Name: ${equipment.equipmentName}`);
                        console.log(`  Created At: ${equipment.createAt}`);
                        console.log(`  Updated At: ${equipment.updateAt}`);
                        console.log(`  Is Deleted: ${equipment.idDeleted}`);
                    });
                    // TODO
                    
                });
            } else {
                console.log(`Error: ${result.message}`);
            }
        })
        .catch(error => console.log('error', error));
}

function bookClassroom() {
    const roomId = 0; // TODO
    const timePeriod = Array.from(document.querySelectorAll('input[name="time-period"]:checked')).map(checkbox => parseInt(checkbox.value));

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "room_id": roomId.parseInt(),
        "time_period": timePeriod
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
                    console.log(`Equipment Name: ${equipment.equipment_name}`);
                });
            } else {
                console.log(`Error: ${result.message}`);
            }
        })
        .catch(error => console.log('error', error));
    // TODO
}
