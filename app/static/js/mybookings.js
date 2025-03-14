document.addEventListener('DOMContentLoaded', async function() {
    const modifyModal = document.querySelector('#modify-modal');
    const applyModifyBtn = document.querySelector('#apply-modify');
    const exportAllBtn = document.querySelector('#export-all-btn');
    const exportSelectedBtn = document.querySelector('#export-selected-btn');

    modifyModal.addEventListener('click', function(event) {
        if (event.target === modifyModal) {
            modifyModal.style.display = 'none';
        }
    });

    applyModifyBtn.addEventListener('click', async function() {
        handleModify();
        modifyModal.style.display = 'none';
    });

    exportAllBtn.addEventListener('click', async function() {
        await getAllReservationAsCalendar();
    });

    exportSelectedBtn.addEventListener('click', async function() {
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
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1>Reservation ID: ${booking.reservationId}</h1>
                            <h3>Room ${booking.roomName}</h3>
                            <h4>Status: ${booking.status}</h4>
                            <p>Date: ${booking.date}</p>
                            <p>Time: ${timeTable[booking.timePeriod]}</p>
                            <p>Capacity: ${booking.capacity}</p>
                            <p>Equipment: ${booking.equipment}</p>
                            <p>Constrain: ${booking.constrain}</p>
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
        btn.addEventListener('click', () => {
            modifyModal.style.display = 'flex';
            checkModifyDate.innerHTML = `${bookings[index].date}`;
            const booking = bookings[index];
            const form = document.querySelector('#modify-form');
            form.elements['reservationId'].value = booking.reservationId;
            form.elements['roomName'].value = booking.roomName;
            form.elements['date'].value = booking.date;
            form.elements['timePeriod'].value = booking.timePeriod;
            form.elements['capacity'].value = booking.capacity;
            form.elements['equipment'].value = booking.equipment;
            form.elements['constrain'].value = booking.constrain;
        });
    });

    cancelBtns.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            handleCancel(bookings[index].reservationId);
        });
    });
}

async function handleModify() {

}

async function handleCancel(reservationId) {

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
    alert(reservationIds)
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