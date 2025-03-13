document.addEventListener('DOMContentLoaded', async function() {
    const modifyModal = document.querySelector('#modify-modal');
    const applyModifyBtn = document.querySelector('#apply-modify');

    modifyModal.addEventListener('click', function(event) {
        if (event.target === modifyModal) {
            modifyModal.style.display = 'none';
        }
    });

    applyModifyBtn.addEventListener('click', async function() {
        handleModify(modifyModal.getAttribute('data-reservation-id'),);
        modifyModal.style.display = 'none';
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
}

async function modifyBooking(reservationId,date,time_period) {
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
                alert('Booking modification successful');
                break;
            default:
                alert(`Error, (${Data.message})`);
        }
    }
    else {
        alert('Error, Network Error');
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
                alert('Booking cancellation successful');
                break;
            default:
                alert(`Error, (${Data.message})`);
        }
    }
    else {
        alert('Error, Network Error');
    }
}

async function viewBookings() {
    const bookings = await getAllMyBookings();
    const bookingList = document.querySelector('.booking-list');
    const timeTable = [
        '8:00~8:45',
        '8:55~9:40',
        '9:50~10:35',
        '10:45~11:30',
        '11:40~12:25',
        '12:35~13:20',
        '13:30~14:15',
        '14:25~15:10',
        '15:20~16:05',
        '16:15~17:00'
      ];

    if(bookings.length > 0) {
        bookingList.innerHTML = '';
        bookings.forEach(booking => {
            const bookingCard = document.createElement('div')
            bookingCard.className = 'booking-card'
            bookingCard.innerHTML = `
                            <h1 class='reservationID' id=${booking.reservationId}>Reservation ID: ${booking.reservationId}</h1>
                            <h3>Room ${booking.roomName}</h3>
                            <h4>Status: ${booking.status}</h4>
                            <p>Date: ${booking.date}</p>
                            <p>Time: ${timeTable[booking.timePeriod]}</p>
                            <p>Capacity: ${booking.capacity}</p>
                            <p>Equipment: ${booking.equipment}</p>
                            <p>Constrain: ${booking.constrain}</p>
                            <button class="action-btn" id="modify-booking">Modify</button>
                            <button class="action-btn" id="cancel-booking">Cancel</button>
                    `;
            bookingList.appendChild(bookingCard);
        });
    }

    const modifyBtns = document.querySelectorAll('#modify-booking');
    const cancelBtns = document.querySelectorAll('#cancel-booking');
    const modifyModal = document.querySelector('#modify-modal');
    const checkModifyDate = document.querySelector('#check-modify-date');

    modifyBtns.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            modifyModal.style.display = 'flex';
            checkModifyDate.innerHTML = `${bookings[index].date}`;
            modifyModal.setAttribute('data-reservation-id', bookings[index].reservationId);
            modifyModal.setAttribute('data-room-available-time', bookings[index].timePeriod);
            document.querySelectorAll('input[name="time-period"]').forEach(checkbox => {
                checkbox.checked = false;
                if (checkbox.value == bookings[index].timePeriod) {
                    checkbox.checked = true;
                }
            });
        });
    });

    cancelBtns.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            handleCancel(bookings[index].reservationId);
        });
    });
}

async function handleModify(reservationId) {
    const date = document.querySelector('#check-modify-date').textContent;
    const time_period = document.querySelector('input[name="time-period"]:checked').value;
    modifyBooking(reservationId,date,time_period);
}

async function handleCancel(reservationId) {
    cancelBooking(reservationId);
}