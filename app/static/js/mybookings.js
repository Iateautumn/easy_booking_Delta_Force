document.addEventListener('DOMContentLoaded', async function () {
    const modifyModal = document.querySelector('#modify-modal');
    const applyModifyBtn = document.querySelector('#apply-modify');
    const exportAllBtn = document.querySelector('#export-all-btn');
    const exportSelectedBtn = document.querySelector('#export-selected-btn');

    modifyModal.addEventListener('click', function (event) {
        if (event.target === modifyModal) {
            modifyModal.style.display = 'none';
        }
    });

    applyModifyBtn.addEventListener('click', async function () {
        handleModify(modifyModal.getAttribute('data-reservation-id'),);
        modifyModal.style.display = 'none';
    });

    exportAllBtn.addEventListener('click', async function () {
        await getAllReservationAsCalendar();
    });

    exportSelectedBtn.addEventListener('click', async function () {
        await getSelectedReservationAsCalendar();
    });

    viewBookings();
});


async function getAllMyBookings() {
    const apiUrl = '/user/reservation';
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

async function modifyBooking(reservationId, date, time_period) {
    const apiUrl = '/user/reservation/modify';
    const userData = {
        'reservation_id': reservationId,
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
            default:
                alert(`Error, (${Data.message})`);
                return false;
        }
    }
    else {
        alert('Error, Network Error');
        return false;
    }
}

async function cancelBooking(reservationId) {
    const apiUrl = '/user/reservation/cancel';
    const userData = {
        'reservation_id': reservationId
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
    }
    else {
        alert('Error, Network Error');
        return false;
    }
}

async function viewBookings() {
    const loading_item = document.getElementById('loading-item');
    loading_item.style.display = 'flex';
    const bookings = await getAllMyBookings();
    const bookingList = document.querySelector('.booking-list');
    const timeTable = [
        '8:00~8:45',
        '8:55~9:40',
        '10:00~10:45',
        '10:55~11:40',
        '14:00~14:45',
        '14:55~15:40',
        '16:00~16:45',
        '16:55~17:40',
        '19:00~19:45',
        '19:55~20:40'
    ];

    if (bookings.length > 0) {
        bookingList.innerHTML = '';
        bookings.forEach(booking => {
            const bookingCard = document.createElement('div')
            if (booking.status === 'Cancelled') {
                bookingCard.style.display = 'none';
            }
            bookingCard.className = 'booking-card'
            bookingCard.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1>Reservation ID: ${booking.reservationId}</h1>
                            <h3>Room ${booking.roomName}</h3>
                            <h4>Status: ${booking.status}</h4>
                            <p>Date: ${booking.date}</p>
                            <p>Time: ${timeTable[booking.timePeriod]}</p>
                            <p>Capacity: ${booking.capacity}</p>
                            <p>Equipment: ${(!booking.equipment || booking.equipment.length == 0) ? 'None' : booking.equipment}</p>
                            <p>Constrain: ${!booking.constrain || booking.constrain == '' ? 'None' : booking.constrain}</p>
                            ${booking.issue ? '<p style="color: #d20000">Issue: ' + booking.issue + '</p>' : ''}
                            <button class="action-btn" id="modify-booking">Modify</button>
                            <button class="action-btn" id="cancel-booking">Cancel</button>
                        </div>
                        <div>
                            <input type="checkbox" class="ui-checkbox" value="${booking.reservationId}">
                        </div>
                    </div>
                    `;
            bookingList.appendChild(bookingCard);
        });
    }

    const modifyBtns = document.querySelectorAll('#modify-booking');
    const cancelBtns = document.querySelectorAll('#cancel-booking');
    const modifyModal = document.querySelector('#modify-modal');
    const checkModifyDate = document.querySelector('#check-modify-date');

    modifyBtns.forEach((btn, index) => {
        btn.addEventListener('click', async () => {
            modifyModal.style.display = 'flex';
            checkModifyDate.innerHTML = `${bookings[index].date}`;
            modifyModal.setAttribute('data-reservation-id', bookings[index].reservationId);
            modifyModal.setAttribute('data-room-available-time', bookings[index].timePeriod);
            availble_time = await getAvailableTime(bookings[index].reservationId);
            document.querySelectorAll('input[name="time-period"]').forEach(checkbox => {
                checkbox.checked = false;
                checkbox.disabled = false;
                if (checkbox.value == bookings[index].timePeriod) {
                    checkbox.checked = true;
                } else if (!availble_time.includes(parseInt(checkbox.value))) {
                    checkbox.disabled = true;
                }
            });
        });
    });

    cancelBtns.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            handleCancel(bookings[index].reservationId);
        });
    });
    loading_item.style.display = 'none';
}

async function getAvailableTime(reservation_id) {
    const apiUrl = '/user/reservation/timeperiod';
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "reservation_id": reservation_id
        }),
    });

    const data = await response.json();

    if (data) {
        switch (data.code) {
            case 200:
                return data.data;
            default:
                alert(`Error, (${data.message})`);
                return [];
        }
    }
    else {
        alert('Error, Network Error');
        return [];
    }
    
}

async function handleModify(reservationId) {
    const date = document.querySelector('#check-modify-date').textContent;
    const time_period = document.querySelector('input[name="time-period"]:checked').value;
    
    const loading_item = document.getElementById('loading-item');
    const bookingList = document.querySelector('.booking-list');
    bookingList.innerHTML = '';

    loading_item.style.display = 'flex';
    document.getElementById('loading-hint').innerText = 'Modifying...';

    const result = await modifyBooking(reservationId, date, time_period);

    document.getElementById('loading-hint').innerText = 'Loading Reservations...';
    if (result) {
        alert('Booking modification successful');
        await viewBookings();
    } else {
        alert('Booking modification failed');
        document.getElementById('loading-item').style.display = 'none';
        await viewBookings();
    }
}

async function handleCancel(reservationId) {

    const loading_item = document.getElementById('loading-item');
    const bookingList = document.querySelector('.booking-list');
    bookingList.innerHTML = '';

    loading_item.style.display = 'flex';
    document.getElementById('loading-hint').innerText = 'Canceling...';

    const result = await cancelBooking(reservationId);

    document.getElementById('loading-hint').innerText = 'Loading Reservations...';

    if (result) {
        alert('Booking cancellation successful');
        viewBookings();
    } else {
        alert('Booking cancellation failed');
        viewBookings();
    }
}

async function getAllReservationAsCalendar() {
    const apiUrl = '/user/calendar';
    await fetch(apiUrl)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'all_reservation.ics';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
}

async function getSelectedReservationAsCalendar() {
    const selectedReservations = document.querySelectorAll('.ui-checkbox:checked');
    const reservationIds = Array.from(selectedReservations).map(checkbox => checkbox.value);
    if (reservationIds.length === 0) {
        alert('Please select at least one reservation');
        return;
    }
    const apiUrl = '/user/calendar';
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "reservation_id": reservationIds
        }),
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'selected_reservation.ics';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}