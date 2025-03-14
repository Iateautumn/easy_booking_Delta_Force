document.addEventListener('DOMContentLoaded', async function() {
    const modifyModal = document.querySelector('#modify-modal');
    const applyModifyBtn = document.querySelector('#apply-modify');

    modifyModal.addEventListener('click', function(event) {
        if (event.target === modifyModal) {
            modifyModal.style.display = 'none';
        }
    });

    applyModifyBtn.addEventListener('click', async function() {
        handleModify();
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