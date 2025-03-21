document.addEventListener('DOMContentLoaded', async function () {
    viewReservations();
});


async function getAllReservations() {
    const apiUrl = '/admin/reservation/all';
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
    else {
        alert('Error, Network Error');
        return [];
    }
}

async function cancelReservation(reservation_id) {
    const apiUrl = '/admin/reservation/cancel';
    const userData = {
        "reservation_id": reservation_id
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

async function viewReservations() {
    const reservations = await getAllReservations();
    const reservationList = document.querySelector('.reservation-list');
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


    if (reservations.length > 0) {
        reservationList.innerHTML = '';
       reservations.forEach(reservation => {
            const reservationCard = document.createElement('div');
            reservationCard.classList.add('room-card');
            reservationCard.innerHTML = `
                <h1>Reservation ID: ${reservation.reservationId}</h1>
                <h3>Room ${reservation.roomName}</h3>
                <h4>User: ${reservation.userName}</h4>
                <p>User Status: ${reservation.status}</p>
                <p>Date: ${reservation.date}</p>
                <p>Time: ${timeTable[reservation.timePeriod]}</p>
                <p>Capacity: ${reservation.capacity}</p>
                <p>Equipment: ${reservation.equipment}</p>
                <p>Constrain: ${(!reservation.constrain || reservation.constrain == '') ? 'None': reservation.constrain}</p>
                ${reservation.issue ? '<p style="color: #d20000">Issue: ' + reservation.issue + '</p>' : ''}
                <button class="action-btn" id="cancel-reservation">Cancel</button>
            `;
            reservationList.appendChild(reservationCard);
        });
    }

    const cancelBtns = document.querySelectorAll('#cancel-reservation');
    console.log(cancelBtns);
    

    cancelBtns.forEach((btn, index) => {
        btn.addEventListener('click', async () => {
            console.log("111");
            const reservation_id = reservations[index].reservationId;
            const result = await cancelReservation(reservation_id);
            if (result) {
                alert('Cancelled');
                viewReservations();
            }
            else {
                alert('Error, Network Error');
            }
        });
    });

}