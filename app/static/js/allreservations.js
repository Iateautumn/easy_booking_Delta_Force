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
        '10:00~10:45',
        '10:55~11:40',
        '14:00~14:45',
        '14:55~15:40',
        '16:00~16:45',
        '16:55~17:40',
        '19:00~19:45',
        '19:55~20:40'
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
                <p>Reservation Status: ${reservation.status}</p>
                <p>Date: ${reservation.date}</p>
                <p>Time: ${timeTable[reservation.timePeriod]}</p>
                <p>Capacity: ${reservation.capacity}</p>
                <p>Equipment: ${(!reservation.equipment || reservation.equipment.length == 0) ? 'None' : reservation.equipment}</p>
                <p>Constraint: ${(!reservation.constrain || reservation.constrain == '') ? 'None': reservation.constrain}</p>
                ${reservation.issue ? '<p style="color: #d20000">Issue: ' + reservation.issue + '</p>' : ''}
                <button class="action-btn" id="cancel-reservation">Cancel</button>
            `;
            reservationList.appendChild(reservationCard);
        });
    }

    const cancelBtns = document.querySelectorAll('#cancel-reservation');
    const loading_item = document.getElementById('loading-item');

    cancelBtns.forEach((btn, index) => {
        btn.addEventListener('click', async () => {

            reservationList.innerHTML = '';

            loading_item.style.display = 'flex';
            document.getElementById('loading-hint').innerText = 'Canceling...';

            const reservation_id = reservations[index].reservationId;
            const result = await cancelReservation(reservation_id);

            document.getElementById('loading-hint').innerText = 'Loading Reservations...';

            if (result) {
                alert('Cancelled');
                viewReservations();
            }
            else {
                alert('Error, Network Error');
                viewReservations();
            }
        });
    });

    
    loading_item.style.display = 'none';

}